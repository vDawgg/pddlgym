"""Implements PDDLEnv, a gym.Env parameterized by PDDL.

One PDDLEnv corresponds to one PDDL domain. Each episode corresponds to
one one PDDL problem; calling env.reset() sets up a new problem.

Observations are namedtuples with attributes `literals`, `objects`, `goal`.
Actions are single ground literals (not operators -- see README).

The debug_info returned by reset and step contains the domain PDDL file
and current problem PDDL file to facilitate interaction with a planner.

Usage example:
>>> env = PDDLEnv("pddl/sokoban.pddl", "pddl/sokoban")
>>> obs, debug_info = env.reset()
>>> action = env.action_space.sample()
>>> obs, reward, done, truncated, debug_info = env.step(action)
"""

from __future__ import annotations

from nl_pddlgym.parser import PDDLDomainParser, PDDLProblemParser, Operator
from nl_pddlgym.inference import find_satisfying_assignments, check_goal
from nl_pddlgym.structs import (
    ground_literal,
    Literal,
    State,
    ProbabilisticEffect,
    LiteralConjunction,
    LiteralDisjunction,
    NoChange,
    ForAll,
    When,
    TypedEntity,
    Predicate,
    DerivedPredicate,
    Type,
)
from nl_pddlgym.spaces import LiteralSpace, LiteralSetSpace, LiteralActionSpace
from nl_pddlgym.prolog_interface import _check_prolog_available

import glob
import os
import typing
from itertools import product
from typing import (
    Optional,
    Union,
    Tuple,
    Dict,
    Set,
    FrozenSet,
    List,
    Callable,
    Any,
    Sequence,
    overload,
)

import gymnasium as gym

import numpy as np


class InvalidAction(Exception):
    """See PDDLEnv docstring"""

    pass


@overload
def get_successor_state(
    state: State,
    action: Literal,
    domain: PDDLDomainParser,
    raise_error_on_invalid_action: bool = ...,
    inference_mode: str = ...,
    require_unique_assignment: bool = ...,
    get_all_transitions: typing.Literal[False] = ...,
    return_probs: typing.Literal[False] = ...,
) -> State: ...


@overload
def get_successor_state(
    state: State,
    action: Literal,
    domain: PDDLDomainParser,
    raise_error_on_invalid_action: bool = ...,
    inference_mode: str = ...,
    require_unique_assignment: bool = ...,
    get_all_transitions: typing.Literal[True] = ...,
    return_probs: bool = ...,
) -> Union[FrozenSet[State], Dict[State, float]]: ...


def get_successor_state(
    state: State,
    action: Literal,
    domain: PDDLDomainParser,
    raise_error_on_invalid_action: bool = False,
    inference_mode: str = "infer",
    require_unique_assignment: bool = True,
    get_all_transitions: bool = False,
    return_probs: bool = False,
) -> Union[State, Dict[State, float], FrozenSet[State]]:
    """
    Compute successor state(s) using operators in the domain

    Parameters
    ----------
    state : State
    action : Literal
    domain : PDDLDomain
    raise_error_on_invalid_action : bool
    inference_mode : "csp" or "prolog" or "infer"
    require_unique_assignment : bool
    get_all_transitions : bool
        If true, this function returns all possible successor states in the case that probabilistic effects exist in the domain.

    Returns
    -------
    next_state : State
    """
    selected_operator, assignment = _select_operator(
        state,
        action,
        domain,
        inference_mode=inference_mode,
        require_unique_assignment=require_unique_assignment,
    )

    # A ground operator was found; execute the ground effects
    if assignment is not None:
        assert selected_operator is not None
        # Get operator effects
        if isinstance(selected_operator.effects, LiteralConjunction):
            effects = selected_operator.effects.literals
        else:
            assert isinstance(selected_operator.effects, Literal)
            effects = [selected_operator.effects]

        next_state = _apply_effects(
            state,
            effects,
            assignment,
            get_all_transitions,
            return_probs=return_probs,
            type_to_parent_types=domain.type_to_parent_types,
        )
        if get_all_transitions:
            return next_state
        assert isinstance(next_state, State)
        state = next_state

    # No operator was found
    elif raise_error_on_invalid_action:
        raise InvalidAction(
            f"called get_successor_state with invalid action '{action}' for given state"
        )

    return state


def get_successor_states(
    state: State,
    action: Literal,
    domain: PDDLDomainParser,
    raise_error_on_invalid_action: bool = False,
    inference_mode: str = "infer",
    require_unique_assignment: bool = True,
    return_probs: bool = False,
) -> Union[FrozenSet[State], Dict[State, float]]:
    result = get_successor_state(
        state,
        action,
        domain,
        raise_error_on_invalid_action,
        inference_mode,
        require_unique_assignment,
        get_all_transitions=True,
        return_probs=return_probs,
    )
    assert not isinstance(result, State)
    return result


def _select_operator(
    state: State,
    action: Literal,
    domain: PDDLDomainParser,
    inference_mode: str = "infer",
    require_unique_assignment: bool = True,
) -> Tuple[Optional[Operator], Optional[Dict[TypedEntity, TypedEntity]]]:
    """
    Helper for successor generation
    """
    if inference_mode == "infer":
        inference_mode = "csp" if _check_domain_for_strips(domain) else "prolog"

    assert domain.operators is not None
    if domain.operators_as_actions:
        # There should be only one possible operator if actions are operators
        possible_operators: set[Operator] = set()
        for name, operator in domain.operators.items():
            if name.lower() == action.predicate.name.lower():
                assert len(possible_operators) == 0
                possible_operators.add(operator)
    else:
        # Possibly multiple operators per action
        possible_operators = set(domain.operators.values())

    # Knowledge base: literals in the state + action taken
    kb = set(state.literals) | {action}

    selected_operator: Optional[Operator] = None
    assignment: Optional[Dict[TypedEntity, TypedEntity]] = None
    for operator in possible_operators:
        if isinstance(operator.preconds, Literal):
            conds = [operator.preconds]
        else:
            conds = operator.preconds.literals
        # Necessary for binding the operator arguments to the variables
        if domain.operators_as_actions:
            conds = [action.predicate(*operator.params)] + conds
        # Check whether action is in the preconditions
        action_literal = None
        for lit in conds:
            if not hasattr(lit, "predicate"):
                continue
            if lit.predicate == action.predicate:
                action_literal = lit
                break
        if action_literal is None:
            continue
        # For proving, consider action variable first
        action_variables = action_literal.variables

        def variable_sort_fn(v):
            return (v not in action_variables, v)

        assignments = find_satisfying_assignments(
            kb,
            conds,
            variable_sort_fn=variable_sort_fn,
            type_to_parent_types=domain.type_to_parent_types,
            constants=domain.constants,
            mode=inference_mode,
        )
        num_assignments = len(assignments)
        if num_assignments > 0:
            selected_operator = operator
            assignment = assignments[0]
            break

    return selected_operator, assignment


def _check_domain_for_strips(domain: PDDLDomainParser) -> bool:
    """
    Check whether all operators in a domain are STRIPS
    """
    assert domain.operators is not None
    for operator in domain.operators.values():
        if not _check_struct_for_strips(operator.preconds):
            return False
    return True


def _check_struct_for_strips(struct: Union[Literal, LiteralConjunction]) -> bool:
    """
    Helper for _check_domain_for_strips
    """
    if isinstance(struct, Literal):
        return True
    if isinstance(struct, LiteralConjunction):
        return all(_check_struct_for_strips(lit) for lit in struct.literals)
    return False


def _ground_literal_safe(
    lifted_lit: Literal, assignments: Dict[TypedEntity, TypedEntity]
) -> Literal:
    """Like ground_literal but tolerates variables that are not in assignments
    (e.g. PDDL constants), leaving them untouched.
    """
    ground_vars = []
    for v in lifted_lit.variables:
        if v in assignments:
            ground_vars.append(assignments[v])
        else:
            ground_vars.append(v)
    return lifted_lit.predicate(*ground_vars)


def _condition_holds(
    cond: Any,
    state_literals: FrozenSet[Literal],
    assignments: Dict[TypedEntity, TypedEntity],
) -> bool:
    """Evaluate a parsed PDDL condition (parsed with is_effect=False) against a
    set of ground state literals, using `assignments` to bind variables to
    objects.

    Supports: Literal (positive/negative, including the built-in `=`
    predicate), LiteralConjunction (and), LiteralDisjunction (or).
    """
    if isinstance(cond, Literal):
        grounded = _ground_literal_safe(cond, assignments)
        if cond.predicate.name == "=":
            a, b = grounded.variables[0], grounded.variables[1]
            equal = a == b
            return equal if not cond.is_negative else (not equal)
        if cond.is_negative:
            return grounded.positive not in state_literals
        return grounded in state_literals
    if isinstance(cond, LiteralConjunction):
        return all(
            _condition_holds(c, state_literals, assignments) for c in cond.literals
        )
    if isinstance(cond, LiteralDisjunction):
        return any(
            _condition_holds(c, state_literals, assignments) for c in cond.literals
        )
    raise NotImplementedError(f"Cannot evaluate condition: {cond}")


def _flatten_effect(
    effect: Any,
    state_literals: FrozenSet[Literal],
    assignments: Dict[TypedEntity, TypedEntity],
    objects: FrozenSet[TypedEntity],
    type_to_parent_types: Optional[Dict[Type, Set[Type]]],
    out: List[Literal],
) -> None:
    """Recursively flatten a lifted effect into a list of ground Literal
    effects appended to `out`. Conditions inside `When` are evaluated against
    `state_literals` (the pre-action state). `ForAll` is grounded by
    enumerating `objects` of the bound variable's type.
    """
    if effect == NoChange():
        return
    if isinstance(effect, LiteralConjunction):
        for lit in effect.literals:
            _flatten_effect(
                lit, state_literals, assignments, objects, type_to_parent_types, out
            )
        return
    if isinstance(effect, ForAll):
        for obj_combo in _forall_object_assignments(
            effect.variables, objects, type_to_parent_types
        ):
            extended = dict(assignments)
            for var, obj in zip(effect.variables, obj_combo):
                extended[var] = obj
            _flatten_effect(
                effect.body,
                state_literals,
                extended,
                objects,
                type_to_parent_types,
                out,
            )
        return
    if isinstance(effect, When):
        if _condition_holds(effect.condition, state_literals, assignments):
            _flatten_effect(
                effect.result,
                state_literals,
                assignments,
                objects,
                type_to_parent_types,
                out,
            )
        return
    # Plain Literal (possibly with is_anti=True for negative effects)
    out.append(_ground_literal_safe(effect, assignments))


def _forall_object_assignments(
    variables: List[TypedEntity],
    objects: FrozenSet[TypedEntity],
    type_to_parent_types: Optional[Dict[Type, Set[Type]]],
) -> List[Tuple[TypedEntity, ...]]:
    """Yield tuples of objects (one per variable) respecting the types of the
    bound variables, including subtype relationships via `type_to_parent_types`.
    Subtype expansion uses the same convention as `get_object_combinations`.
    """
    type_to_objs: Dict[Any, List[TypedEntity]] = {}
    for obj in sorted(objects):
        if type_to_parent_types is None:
            type_to_objs.setdefault(obj.var_type, []).append(obj)
        else:
            for t in type_to_parent_types.get(obj.var_type, {obj.var_type}):
                type_to_objs.setdefault(t, []).append(obj)
    choices = [type_to_objs.get(var.var_type, []) for var in variables]
    return [c for c in product(*choices)]


def _compute_new_state_from_lifted_effects(
    lifted_effects: List[Any],
    assignments: Dict[TypedEntity, TypedEntity],
    new_literals: Set[Literal],
    state_literals: Optional[FrozenSet[Literal]] = None,
    objects: Optional[FrozenSet[TypedEntity]] = None,
    type_to_parent_types: Optional[Dict[Type, Set[Type]]] = None,
) -> Set[Literal]:
    # When state/objects context is available, flatten conditional (When) and
    # universal (ForAll) effects into a list of already-ground Literals; this
    # also evaluates each `When` condition against the pre-action state.
    # Otherwise (legacy path) the caller passes only plain lifted Literals and
    # we ground them here.
    if state_literals is not None and objects is not None:
        flat_effects: List[Literal] = []
        for lifted_effect in lifted_effects:
            _flatten_effect(
                lifted_effect,
                state_literals,
                assignments,
                objects,
                type_to_parent_types,
                flat_effects,
            )
        # flat_effects are already ground; apply two-pass remove/add directly.
        for effect in flat_effects:
            if effect == NoChange():
                continue
            if effect.is_anti:
                literal = effect.inverted_anti
                if literal in new_literals:
                    new_literals.remove(literal)
        for effect in flat_effects:
            if effect == NoChange():
                continue
            if not effect.is_anti:
                new_literals.add(effect)
        return new_literals
    # Legacy path: lifted_effects are plain lifted Literals.
    for lifted_effect in lifted_effects:
        if lifted_effect == NoChange():
            continue
        effect = ground_literal(lifted_effect, assignments)
        # Negative effect
        if effect.is_anti:
            literal = effect.inverted_anti
            if literal in new_literals:
                new_literals.remove(literal)
    for lifted_effect in lifted_effects:
        if lifted_effect == NoChange():
            continue
        effect = ground_literal(lifted_effect, assignments)
        if not effect.is_anti:
            new_literals.add(effect)
    return new_literals


def _apply_effects(
    state: State,
    lifted_effects: Sequence[Union[Literal, ProbabilisticEffect]],
    assignments: Dict[TypedEntity, TypedEntity],
    get_all_transitions: bool = False,
    return_probs: bool = False,
    type_to_parent_types: Optional[Dict[Type, Set[Type]]] = None,
) -> Union[State, Dict[State, float], FrozenSet[State]]:
    """
    Update a state given lifted operator effects and
    assignments of variables to objects.

    Parameters
    ----------
    state : State
        The state on which the effects are applied.
    lifted_effects : { Literal }
    assignments : { TypedEntity : TypedEntity }
        Maps variables to objects.
    get_all_transitions : bool
        If true, this function returns all possible successor states in the
        case that probabilistic effects exist in the domain.
    type_to_parent_types : dict, optional
        Type hierarchy used to ground ForAll effects over subtypes. When
        omitted, only objects whose `var_type` exactly matches the bound
        variable's type are enumerated.
    """
    new_literals = set(state.literals)
    determinized_lifted_effects: List[Any] = []
    # Handle probabilistic effects.

    # Each element of this list contain
    #   a pair of outcomes from a probabilistic effect
    probabilistic_lifted_effects: List[List[Literal]] = []
    for lifted_effect in lifted_effects:
        if isinstance(lifted_effect, ProbabilisticEffect):
            effect_outcomes = lifted_effect.literals
            probas = dict(zip(lifted_effect.literals, lifted_effect.probabilities))
            cur_probabilistic_lifted_effects: List[Literal] = []

            if get_all_transitions:
                lifted_effects_list = cur_probabilistic_lifted_effects
            else:
                lifted_effects_list = determinized_lifted_effects
            sampled_effect = lifted_effect.sample()

            # If get_all_transitions == False, create list with sampled state only
            # Otherwise, populate it with possible outcomes
            effects_to_process = (
                [sampled_effect] if not get_all_transitions else effect_outcomes
            )

            for chosen_effect in effects_to_process:
                if isinstance(chosen_effect, LiteralConjunction):
                    for lit in chosen_effect.literals:
                        lifted_effects_list.append(lit)
                        lit.proba = probas[chosen_effect]
                else:
                    lifted_effects_list.append(chosen_effect)
                    chosen_effect.proba = probas[chosen_effect]

            if get_all_transitions:
                probabilistic_lifted_effects.append(cur_probabilistic_lifted_effects)
        elif isinstance(lifted_effect, (ForAll, When, LiteralConjunction)):
            # Conditional (when) and universal (forall) effects are flattened
            # inside _compute_new_state_from_lifted_effects using the state.
            determinized_lifted_effects.append(lifted_effect)
        else:
            assert isinstance(lifted_effect, Literal)
            determinized_lifted_effects.append(lifted_effect)

    states: List[State] = []
    if not get_all_transitions:
        new_literals = _compute_new_state_from_lifted_effects(
            determinized_lifted_effects,
            assignments,
            new_literals,
            state_literals=state.literals,
            objects=state.objects,
            type_to_parent_types=type_to_parent_types,
        )

        return state.with_literals(new_literals)

    # else - get all possible transitions

    # Construct combinations of probabilistic effects
    probabilistic_effects_combinations = list(product(*probabilistic_lifted_effects))

    states_to_probs: Dict[State, float] = {}
    for prob_efs_combination in probabilistic_effects_combinations:
        total_proba = np.prod([lit.proba for lit in prob_efs_combination])
        if total_proba == 0:
            continue
        new_prob_literals = set(state.literals)
        new_determinized_lifted_effects = determinized_lifted_effects + list(
            prob_efs_combination
        )
        new_prob_literals = _compute_new_state_from_lifted_effects(
            new_determinized_lifted_effects,
            assignments,
            new_prob_literals,
            state_literals=state.literals,
            objects=state.objects,
            type_to_parent_types=type_to_parent_types,
        )

        new_state = state.with_literals(new_prob_literals)
        if new_state in states_to_probs:
            # If there are multiple ways of reaching next state,
            #   then these probabilities have to be summed
            states_to_probs[new_state] += total_proba
        else:
            states_to_probs[new_state] = total_proba
        states.append(new_state)
    if return_probs:
        return states_to_probs
    # convert list of states to set
    return frozenset(states)


class PDDLEnv(gym.Env[State, Literal]):
    """
    Parameters
    ----------
    domain_file : str
        Path to a PDDL domain file.
    problem_dir : str
        Path to a directory of PDDL problem files.
    render : fn or None
        An optional render function (obs -> img).
    seed : int
        Random seed used to sample new problems upon reset.
    raise_error_on_invalid_action : bool
        When an action is taken for which no operator's
        preconditions holds, raise InvalidAction() if True;
        otherwise silently make no changes to the state.
    operators_as_actions : bool
        If True, the PDDL operators are treated as the actions.
        Otherwise, actions must be specified separately in the PDDL file.
    dynamic_action_space : bool
        Let self.action_space dynamically change on each iteration to
        include only valid actions (must match operator preconditions).
    """

    metadata: Dict[str, Any] = {"render_modes": []}
    reward_range: Tuple[float, float] = (-float("inf"), float("inf"))
    spec: Any = None

    _state: Optional[State]
    _domain_file: str
    _problem_dir: str
    _render: Optional[Callable[..., Any]]
    _raise_error_on_invalid_action: bool
    operators_as_actions: bool
    _problem_index_fixed: bool
    _problem_idx: Optional[int]
    _seed: int
    rng: np.random.RandomState
    domain: PDDLDomainParser
    problems: List[PDDLProblemParser]
    _domain_is_strips: bool
    _inference_mode: str
    _contains_derived_predicates: bool
    action_predicates: List[Predicate]
    _dynamic_action_space: bool
    _action_space: LiteralSpace
    _observation_space: LiteralSetSpace
    _problem: PDDLProblemParser
    _goal: Any

    def __init__(
        self,
        domain_file: str,
        problem_dir: str,
        render: Optional[Callable[..., Any]] = None,
        seed: int = 0,
        raise_error_on_invalid_action: bool = False,
        operators_as_actions: bool = False,
        dynamic_action_space: bool = False,
    ) -> None:
        self._state: Optional[State] = None
        self._domain_file: str = domain_file
        self._problem_dir: str = problem_dir
        self._render: Optional[Callable[..., Any]] = render
        self.seed(seed)
        self._raise_error_on_invalid_action: bool = raise_error_on_invalid_action
        self.operators_as_actions: bool = operators_as_actions

        # Set by self.fix_problem_index
        self._problem_index_fixed: bool = False

        self._problem_idx: Optional[int] = None

        # Parse the PDDL files
        self.domain, self.problems = self.load_pddl(
            domain_file, problem_dir, operators_as_actions=self.operators_as_actions
        )

        # Determine if the domain is STRIPS
        self._domain_is_strips: bool = _check_domain_for_strips(self.domain)
        self._inference_mode: str = "csp" if self._domain_is_strips else "prolog"
        # Some domains require prolog. We want to avoid users running
        # inference on a large chunk of the dataset and only failing
        # once we hit prolog domains. Due to this, we call this early
        # as to not fail too late.
        _check_prolog_available()

        # Determine if domain contains derived predicates
        self._contains_derived_predicates: bool = any(
            p.is_derived for p in self.domain.predicates.values()
        )

        # Initialize action space with problem-independent components
        actions = list(self.domain.actions)
        self.action_predicates: List[Predicate] = [
            self.domain.predicates[a] for a in actions
        ]
        self._dynamic_action_space: bool = dynamic_action_space
        if dynamic_action_space:
            if self.domain.operators_as_actions and self._domain_is_strips:
                self._action_space: LiteralSpace = LiteralActionSpace(
                    self.domain,
                    self.action_predicates,
                    type_hierarchy=self.domain.type_hierarchy,
                    type_to_parent_types=self.domain.type_to_parent_types,
                )
            else:
                self._action_space = LiteralSpace(
                    self.action_predicates,
                    lit_valid_test=self._action_valid_test,
                    type_hierarchy=self.domain.type_hierarchy,
                    type_to_parent_types=self.domain.type_to_parent_types,
                )

        else:
            self._action_space = LiteralSpace(
                self.action_predicates,
                type_to_parent_types=self.domain.type_to_parent_types,
            )

        # Initialize observation space with problem-independent components
        self._observation_space: LiteralSetSpace = LiteralSetSpace(
            list(set(self.domain.predicates.values()) - set(self.action_predicates)),
            type_hierarchy=self.domain.type_hierarchy,
            type_to_parent_types=self.domain.type_to_parent_types,
        )

    @staticmethod
    def load_pddl(
        domain_file: str, problem_dir: str, operators_as_actions: bool = False
    ) -> Tuple[PDDLDomainParser, List[PDDLProblemParser]]:
        """
        Parse domain and problem PDDL files.

        Parameters
        ----------
        domain_file : str
            Path to a PDDL domain file.
        problem_dir : str
            Path to a directory of PDDL problem files.
        operators_as_actions : bool
            See class docstirng.

        Returns
        -------
        domain : PDDLDomainParser
        problems : [ PDDLProblemParser ]
        """
        domain = PDDLDomainParser(
            domain_file,
            expect_action_preds=(not operators_as_actions),
            operators_as_actions=operators_as_actions,
        )
        problems: List[PDDLProblemParser] = []
        problem_files = [f for f in glob.glob(os.path.join(problem_dir, "*.pddl"))]
        for problem_file in sorted(problem_files):
            assert domain.domain_name is not None
            problem = PDDLProblemParser(
                problem_file,
                domain.domain_name,
                domain.types,
                domain.predicates,
                domain.actions,
                domain.constants,
            )
            problems.append(problem)
        return domain, problems

    @property
    def observation_space(self) -> LiteralSetSpace:
        return self._observation_space

    @property
    def action_space(self) -> LiteralSpace:
        return self._action_space

    def set_state(self, state: State) -> None:
        self._state = state

    def get_state(self) -> Optional[State]:
        return self._state

    def seed(self, seed: int) -> None:
        self._seed = seed
        self.rng = np.random.RandomState(seed)

    def fix_problem_index(self, problem_idx: int) -> None:
        """
        Fix the PDDL problem used when reset is called.

        Useful for reproducible testing.

        The order of PDDL problems is determined by the names
        of their files. See PDDLEnv.load_pddl.

        The given index is treated as a human-readable problem number
        (e.g., 8 for problem8.pddl) and automatically converted to the
        correct alphabetical file index.

        Parameters
        ----------
        problem_idx : int
        """
        if self.problems:
            import os

            sorted_fnames = sorted(
                os.path.basename(p.problem_fname) for p in self.problems
            )
            for candidate in [
                f"problem{problem_idx}.pddl",
                f"prob{problem_idx:02d}.pddl",
                f"pfile{problem_idx}.pddl",
            ]:
                if candidate in sorted_fnames:
                    problem_idx = sorted_fnames.index(candidate)
                    break
        self._problem_idx = problem_idx
        self._problem_index_fixed = True

    def reset(
        self, seed: Optional[int] = None, options: Optional[Dict[str, Any]] = None
    ) -> Tuple[State, Dict[str, Any]]:
        """
        Set up a new PDDL problem and start a new episode.

        Note that the PDDL files are included in debug_info.

        Returns
        -------
        obs : { Literal }
            The set of active predicates.
        debug_info : dict
            See self._get_debug_info()
        """
        if seed is not None:
            self.seed(seed)

        if not self._problem_index_fixed:
            self._problem_idx = self.rng.choice(len(self.problems))
        assert self._problem_idx is not None
        self._problem = self.problems[self._problem_idx]

        assert self._problem.initial_state is not None
        assert self._problem.objects is not None
        initial_state = State(
            frozenset(self._problem.initial_state),
            frozenset(self._problem.objects),
            self._problem.goal,
        )
        initial_state = self._handle_derived_literals(initial_state)
        self.set_state(initial_state)

        self._goal = self._problem.goal
        debug_info = self._get_debug_info()

        self._action_space.reset_initial_state(initial_state)

        return_state = self.get_state()
        assert return_state is not None
        return return_state, debug_info

    def _get_debug_info(self) -> Dict[str, str]:
        """
        Contains the problem file and domain file
        for interaction with a planner.
        """
        info: Dict[str, str] = {
            "problem_file": self._problem.problem_fname,
            "domain_file": self.domain.domain_fname,
        }
        return info

    def step(self, action: Literal) -> Tuple[State, float, bool, bool, Dict[str, Any]]:
        """
        Execute an action and update the state.

        Tries to find a ground operator for which the
        preconditions hold when this action is taken. If none
        exist, optionally raises InvalidAction. If multiple
        exist, raises an AssertionError, since we assume
        deterministic environments only. Once the operator
        is found, the ground effects are executed to update
        the state.

        Parameters
        ----------
        action : Literal

        Returns
        -------
        state : State
            The set of active predicates.
        reward : float
            1 if the goal is reached and 0 otherwise.
        done : bool
            True if the goal is reached.
        truncated : bool
            Whether a truncation condition outside the scope of the MDP is satisfied. This never happens, so set to False.
        debug_info : dict
            See self._get_debug_info.
        """
        state, reward, done, debug_info = self.sample_transition(action)
        self.set_state(state)
        return state, reward, done, False, debug_info

    def _get_new_state_info(
        self, state: State
    ) -> Tuple[State, float, bool, Dict[str, Any]]:
        state = self._handle_derived_literals(state)

        done = self._is_goal_reached(state)

        reward = self.extrinsic_reward(state, done)
        debug_info = self._get_debug_info()

        return state, reward, done, debug_info

    def sample_transition(
        self, action: Literal
    ) -> Tuple[State, float, bool, Dict[str, Any]]:
        state = self._get_successor_state(
            self._state,
            action,
            self.domain,
            inference_mode=self._inference_mode,
            raise_error_on_invalid_action=self._raise_error_on_invalid_action,
        )
        assert isinstance(state, State)
        return self._get_new_state_info(state)

    def _get_successor_state(
        self, *args: Any, **kwargs: Any
    ) -> Union[State, Dict[State, float], FrozenSet[State]]:
        """Separated out to allow for overrides in subclasses"""
        return get_successor_state(*args, **kwargs)

    def _get_successor_states(
        self, *args: Any, **kwargs: Any
    ) -> Union[FrozenSet[State], Dict[State, float]]:
        """Separated out to allow for overrides in subclasses"""
        return get_successor_states(*args, **kwargs)

    def get_all_possible_transitions(self, action: Literal, return_probs: bool = False):
        assert self.domain.is_probabilistic
        assert self._state is not None
        states = self._get_successor_states(
            self._state,
            action,
            self.domain,
            inference_mode=self._inference_mode,
            raise_error_on_invalid_action=self._raise_error_on_invalid_action,
            return_probs=return_probs,
        )
        if return_probs:
            assert isinstance(states, dict)
            return [
                (self._get_new_state_info(state), prob)
                for state, prob in states.items()
            ]

        assert isinstance(states, frozenset)
        return [self._get_new_state_info(state) for state in states]

    def extrinsic_reward(self, state: State, done: bool) -> float:
        if done:
            reward = 1.0
        else:
            reward = 0.0

        return reward

    def _is_goal_reached(self, state: State) -> bool:
        """
        Check if the terminal condition is met, i.e., the goal is reached.
        """
        return check_goal(state, self._goal)

    def _action_valid_test(self, state: State, action: Literal) -> bool:
        _, assignment = _select_operator(
            state, action, self.domain, inference_mode=self._inference_mode
        )
        return assignment is not None

    def render(self, *args: Any, **kwargs: Any) -> Any:
        if self._render and self._state is not None:
            return self._render(self._state.literals, *args, **kwargs)

    def _handle_derived_literals(self, state: State) -> State:
        # no need to compute derived predicates if there are none
        if not self._contains_derived_predicates:
            return state

        # first remove any old derived literals since they're outdated
        to_remove: Set[Literal] = set()
        for lit in state.literals:
            if lit.predicate.is_derived:
                to_remove.add(lit)
        state = state.with_literals(state.literals - to_remove)

        # add negative basic literals for checking derived predicates
        state_literals = set(state.literals)
        all_ground_literals = self._observation_space.all_ground_literals(state)
        for lit in all_ground_literals:
            if not lit.predicate.is_derived and lit not in state_literals:
                state_literals = {lit.negative} | state_literals

        while True:  # loop, because derived predicates can be recursive
            new_derived_literals: Set[Literal] = set()
            for pred in self.domain.predicates.values():
                if not pred.is_derived:
                    continue
                derived_pred = typing.cast(DerivedPredicate, pred)
                assert derived_pred.body is not None
                assert derived_pred.param_names is not None
                assert derived_pred.var_types is not None
                assignments = find_satisfying_assignments(
                    state_literals,
                    derived_pred.body,
                    type_to_parent_types=self.domain.type_to_parent_types,
                    constants=self.domain.constants,
                    mode="prolog",
                    max_assignment_count=99999,
                )
                for assignment in assignments:
                    objects = [
                        assignment[param_type(param_name)]
                        for param_name, param_type in zip(
                            derived_pred.param_names, derived_pred.var_types
                        )
                    ]
                    derived_literal = pred(*objects)
                    if derived_literal not in state.literals:
                        new_derived_literals.add(derived_literal)
            if new_derived_literals:
                # update state_literals for recursive checking
                state_literals = state_literals | new_derived_literals
                # save derived literals in state
                state = state.with_literals(state.literals | new_derived_literals)
            else:  # terminate
                break
        return state
