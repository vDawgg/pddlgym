"""Python classes for common PDDL structures"""

from __future__ import annotations

from collections import namedtuple
from typing import Any, ClassVar, cast, overload
import numpy as np


### PDDL Types, Objects, Variables ###
class Type(str):
    """A PDDL type"""

    is_continuous: ClassVar[bool] = False

    def __call__(self, entity_name: str) -> TypedEntity:
        return TypedEntity.__new__(TypedEntity, entity_name, self)


# Default type
NULLTYPE: Type = Type("null")


class TypedEntity(str):
    """All objects and variables from PDDL are TypedEntitys"""

    name: str
    var_type: Type
    _str: str
    is_continuous: bool

    def __new__(cls, name: str, var_type: Type) -> TypedEntity:
        assert isinstance(var_type, Type)
        obj = str.__new__(cls, name)
        obj.name = name
        obj.var_type = var_type
        obj._str = str(obj.name) + ":" + str(obj.var_type)
        obj.is_continuous = False
        return obj

    def __str__(self) -> str:
        return self._str

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __add__(self, other: Any) -> str:
        return str(self) + str(other)

    def __radd__(self, other: Any) -> str:
        return str(other) + str(self)

    def __copy__(self) -> TypedEntity:
        return self

    def __deepcopy__(self, memo: Any) -> TypedEntity:
        return self

    def __getnewargs_ex__(self) -> tuple[tuple[str, Type], dict]:
        return ((self.name, self.var_type), {})


### Predicates ###
class Predicate(object):
    """
    A Predicate is a factory for Literals.

    Parameters
    ----------
    name : str
    arity : int
        The number of variables in the predicate.
    var_types : [ Type ]
        The Type of each variable in the predicate.
    is_negative : bool
        Whether this Predicate is negative (as in a
        negative precondition).
    is_anti : bool
        Whether this Predicate is anti (as in a
        negative effect).
    """

    name: str
    arity: int
    var_types: list[Type] | None
    is_negative: bool
    negated_as_failure: bool
    is_anti: bool
    is_derived: bool

    def __init__(
        self,
        name: str,
        arity: int,
        var_types: list[Type] | None = None,
        is_negative: bool = False,
        is_anti: bool = False,
        negated_as_failure: bool = False,
    ) -> None:
        self.name = name
        self.arity = arity
        self.var_types = var_types
        self.is_negative = is_negative
        self.negated_as_failure = negated_as_failure
        self.is_anti = is_anti
        self.is_derived = False

    def __call__(self, *variables: TypedEntity | str) -> Literal:
        var_list = list(variables)
        assert len(var_list) == self.arity
        return Literal(self, var_list)

    def __str__(self) -> str:
        if self.negated_as_failure:
            neg_prefix = "~"
        elif self.is_negative:
            neg_prefix = "Not"
        elif self.is_anti:
            neg_prefix = "Anti"
        else:
            neg_prefix = ""
        return neg_prefix + self.name

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other)

    def __lt__(self, other: Any) -> bool:
        return str(self) < str(other)

    def __gt__(self, other: Any) -> bool:
        return str(self) > str(other)

    @property
    def positive(self) -> Predicate:
        return self.__class__(
            self.name, self.arity, self.var_types, is_anti=self.is_anti
        )

    @property
    def negative(self) -> Predicate:
        return self.__class__(
            self.name,
            self.arity,
            self.var_types,
            is_negative=True,
            is_anti=self.is_anti,
        )

    @property
    def inverted_anti(self) -> Predicate:
        assert not self.is_negative
        return self.__class__(
            self.name, self.arity, self.var_types, is_anti=(not self.is_anti)
        )

    def negate_as_failure(self) -> Predicate:
        assert not self.negated_as_failure
        return Predicate(
            self.name,
            self.arity,
            self.var_types,
            negated_as_failure=True,
            is_anti=self.is_anti,
        )

    def pddl_variables(self) -> list[str]:
        variables = []
        if self.var_types:
            for i, vt in enumerate(self.var_types):
                v = "?v{} - {}".format(i, vt)
                variables.append(v)
        else:
            for i in range(self.arity):
                v = "?v{}".format(i)
                variables.append(v)
        return variables

    def pddl_str(self) -> str:
        if self.var_types and len(self.var_types) > 0:
            var_str = " " + " ".join(self.pddl_variables())
        elif not self.var_types and self.arity > 0:
            var_str = " " + " ".join(self.pddl_variables())
        else:
            var_str = ""
        if self.is_anti:
            return "(not ({}{}))".format(self.inverted_anti, var_str)
        if self.is_negative:
            return "(not ({}{}))".format(self.positive, var_str)
        if self.negated_as_failure:
            raise NotImplementedError
        return "({}{})".format(self, var_str)


class DerivedPredicate(Predicate):
    param_names: list[str] | None
    body: Any | None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.is_derived = True
        self.param_names = None
        self.body = None

    def setup(self, param_names: list[str], body: Any) -> None:
        self.param_names = param_names
        assert self.param_names is not None
        assert self.var_types is not None
        assert len(self.param_names) == len(self.var_types)
        self.body = body

    def derived_pddl_str(self) -> str:
        assert self.param_names is not None
        assert self.body is not None
        if len(self.param_names) > 0:
            param_str = " " + " ".join(self.param_names)
        else:
            param_str = ""
        return "(:derived ({}{}) {})".format(self.name, param_str, self.body.pddl_str())


### Literals ###
class Literal:
    """A literal is a relation between objects or variables.

    Both lifted literals (ones with variables) and ground
    literals (ones with objects) are Literals in this code.

    Parameters
    ----------
    predicate : Predicate
    variables : [ TypedEntity or str ]
    """

    predicate: Predicate
    variables: list[TypedEntity]
    is_negative: bool
    is_anti: bool
    negated_as_failure: bool
    proba: float = 0.0
    _str: str

    def __init__(
        self, predicate: Predicate, variables: list[TypedEntity | str]
    ) -> None:
        self.predicate = predicate
        self.variables = cast(list[TypedEntity], variables)
        self.is_negative = predicate.is_negative
        self.is_anti = predicate.is_anti
        self.negated_as_failure = predicate.negated_as_failure

        # Apply types to untyped objects
        if self.predicate.var_types is not None:
            for i, (expected_type, var) in enumerate(
                zip(self.predicate.var_types, self.variables)
            ):
                if not hasattr(var, "var_type"):
                    # Convert strings
                    self.variables[i] = expected_type(var)

        # Cache str for repr
        self._str = str(self.predicate) + "(" + ",".join(map(str, self.variables)) + ")"

    def set_variables(self, variables: list[TypedEntity]) -> None:
        self.variables = variables
        self._update_variable_caches()

    def update_variable(self, var_idx: int, new_value: TypedEntity) -> None:
        self.variables[var_idx] = new_value
        self._update_variable_caches()

    def _update_variable_caches(self) -> None:
        # Recompute cache
        self._str = str(self.predicate) + "(" + ",".join(map(str, self.variables)) + ")"

    def __str__(self) -> str:
        return self._str

    def __repr__(self) -> str:
        return self._str

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        return repr(self) == repr(other)

    def __lt__(self, other: Any) -> bool:
        return repr(self) < repr(other)

    def __gt__(self, other: Any) -> bool:
        return repr(self) > repr(other)

    def holds(self, state_literals: set | frozenset) -> bool:
        raise NotImplementedError("Goals can only be LiteralConjunctions")

    @property
    def positive(self) -> Literal:
        return self.__class__(self.predicate.positive, [v for v in self.variables])

    @property
    def negative(self) -> Literal:
        return self.__class__(self.predicate.negative, [v for v in self.variables])

    @property
    def inverted_anti(self) -> Literal:
        return self.__class__(self.predicate.inverted_anti, [v for v in self.variables])

    def negate_as_failure(self) -> Literal:
        if self.negated_as_failure:
            return self.positive
        naf_predicate = self.predicate.negate_as_failure()
        return naf_predicate(*self.variables)

    def pddl_variables(self) -> list[str]:
        return [
            v.replace("(", "").replace(")", "").replace(",", "") for v in self.variables
        ]

    def pddl_variables_typed(self) -> list[str]:
        return [
            str(v)
            .replace("(", "")
            .replace(")", "")
            .replace(",", "")
            .replace(":", " - ")
            for v in self.variables
        ]

    def pddl_str(self) -> str:
        if len(self.variables) > 0:
            var_str = " " + " ".join(self.pddl_variables())
        else:
            var_str = ""
        if self.is_anti:
            return "(not ({}{}))".format(self.predicate.inverted_anti, var_str)
        if self.is_negative:
            return "(not ({}{}))".format(self.predicate.positive, var_str)
        if self.negated_as_failure:
            raise NotImplementedError
        return "({}{})".format(self.predicate, var_str)


class LiteralConjunction:
    """A logical conjunction (AND) of Literals.

    Parameters
    ----------
    literals : [ Literal ]
    """

    literals: list[Literal]

    def __init__(self, literals: list[Literal]) -> None:
        self.literals = literals

    def pddl_variables(self) -> set:
        return set().union(*(lit.pddl_variables() for lit in self.literals))

    def pddl_variables_typed(self) -> set:
        return set().union(*(lit.pddl_variables_typed() for lit in self.literals))

    def pddl_str(self) -> str:
        return "(and\n\t{})".format(
            "\n\t".join(lit.pddl_str() for lit in self.literals)
        )

    def holds(self, state_literals: set | frozenset) -> bool:
        print("Deprecation warning: LiteralConjunction.holds will be removed soon")
        assert isinstance(state_literals, (set, frozenset))
        for lit in self.literals:
            assert not lit.is_anti
            if lit in state_literals and lit.is_negative:
                return False
            if lit not in state_literals and not lit.is_negative:
                return False
        return True

    def __str__(self) -> str:
        return "AND{}".format(self.literals)

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other)


class LiteralDisjunction:
    """A logical disjunction (OR) of Literals.

    Parameters
    ----------
    literals : [ Literal ]
    """

    literals: list[Literal]

    def __init__(self, literals: list[Literal]) -> None:
        self.literals = literals

    def pddl_variables(self) -> set:
        return set().union(*(lit.pddl_variables() for lit in self.literals))

    def pddl_variables_typed(self) -> set:
        return set().union(*(lit.pddl_variables_typed() for lit in self.literals))

    def pddl_str(self) -> str:
        return "(or\n\t{})".format("\n\t".join(lit.pddl_str() for lit in self.literals))

    def holds(self, state_literals: set | frozenset) -> bool:
        raise NotImplementedError("Goals can only be LiteralConjunctions")

    def __str__(self) -> str:
        return "OR{}".format(self.literals)

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other)


class ForAll:
    """Represents a ForAll over the given variable in the given literal.
    variable is a structs.TypedEntity.
    """

    body: Any
    variables: list
    is_negative: bool

    def __init__(
        self, body: Any, variables: str | list, is_negative: bool = False
    ) -> None:
        if isinstance(variables, str):
            variables = [variables]

        self.body = body
        self.variables = variables
        self.is_negative = is_negative

    def __str__(self) -> str:
        forall_str = "FORALL ({}) : {}".format(self.variables, self.body)
        if self.is_negative:
            return "NOT-" + forall_str
        return forall_str

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other)

    @property
    def positive(self) -> ForAll:
        return ForAll(self.body, self.variables)

    def pddl_str(self) -> str:
        body_str = self.body.pddl_str()
        var_str = "\n".join(
            ["{} - {}".format(v.name, v.var_type) for v in self.variables]
        )
        forall_str = "(forall ({}) {})".format(var_str, body_str)
        if self.is_negative:
            return "(not {})".format(forall_str)
        return forall_str


class Exists:
    """ """

    variables: list
    body: Any
    is_negative: bool

    def __init__(self, variables: list, body: Any, is_negative: bool = False) -> None:
        self.variables = variables
        self.body = body
        self.is_negative = is_negative

    def __str__(self) -> str:
        exists_str = "EXISTS ({}) : {}".format(self.variables, str(self.body))
        if self.is_negative:
            return "NOT-" + exists_str
        return exists_str

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other)

    @property
    def positive(self) -> Exists:
        return Exists(self.variables, self.body)

    def pddl_str(self) -> str:
        body_str = self.body.pddl_str()
        var_str = "\n".join(
            ["{} - {}".format(v.name, v.var_type) for v in self.variables]
        )
        exists_str = "(exists ({}) {})".format(var_str, body_str)
        if self.is_negative:
            return "(not {})".format(exists_str)
        return exists_str


class ProbabilisticEffect:
    """Represents a probabilistic effect over a set of possibilities."""

    literals: list[Literal]
    probabilities: list[float]

    def __init__(self, literals: list[Literal], probabilities: list[float]) -> None:
        self.literals = literals
        self.probabilities = probabilities
        assert sum(self.probabilities) <= 1.0
        self.literals.append(NoChange())
        self.probabilities.append(1 - sum(self.probabilities))

    def __str__(self) -> str:
        return "PROBABILISTIC{}".format(list(zip(self.literals, self.probabilities)))

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other)

    def pddl_str(self) -> str:
        raise NotImplementedError("Can't PDDL-ify a probabilistic effect")

    def sample(self) -> Any:
        return np.random.choice(cast(list[Any], self.literals), p=self.probabilities)

    def max(self) -> Any:
        return self.literals[np.argmax(self.probabilities)]


### States ###


# A State is a frozenset of ground literals and a frozenset of objects
class State(namedtuple("State", ["literals", "objects", "goal"])):
    __slots__ = ()
    """A State is a frozenset of ground literals and a frozenset of objects"""

    def with_literals(self, literals: Any) -> State:
        """
        Return a new state that has the same objects and goal as the given one,
        but has the given set of literals instead of state.literals.
        """
        return self._replace(literals=frozenset(literals))

    def with_objects(self, objects: Any) -> State:
        """
        Return a new state that has the same literals and goal as the given one,
        but has the given set of objects instead of state.objects.
        """
        return self._replace(objects=frozenset(objects))

    def with_goal(self, goal: Any) -> State:
        """
        Return a new state that has the same literals and objects as the given
        one, but has the given goal instead of state.goal.
        """
        return self._replace(goal=goal)


### Helpers ###
@overload
def Not(x: Predicate) -> Predicate: ...
@overload
def Not(x: Literal) -> Literal: ...
@overload
def Not(x: ForAll) -> ForAll: ...
@overload
def Not(x: Exists) -> Exists: ...
@overload
def Not(x: LiteralConjunction) -> LiteralDisjunction: ...
@overload
def Not(x: LiteralDisjunction) -> LiteralConjunction: ...
def Not(x):  # pylint:disable=invalid-name
    """Negate a Predicate or Literal."""
    if isinstance(x, Predicate):
        return Predicate(
            x.name,
            x.arity,
            var_types=x.var_types,
            is_negative=(not x.is_negative),
            is_anti=(x.is_anti),
        )

    if isinstance(x, ForAll):
        return ForAll(x.body, x.variables, is_negative=(not x.is_negative))

    if isinstance(x, Exists):
        return Exists(x.variables, x.body, is_negative=(not x.is_negative))

    if isinstance(x, LiteralConjunction):
        return LiteralDisjunction([Not(lit) for lit in x.literals])

    if isinstance(x, LiteralDisjunction):
        return LiteralConjunction([Not(lit) for lit in x.literals])

    assert isinstance(x, Literal)
    new_predicate = Not(x.predicate)
    return new_predicate(*x.variables)


@overload
def Anti(x: Predicate) -> Predicate: ...
@overload
def Anti(x: Literal) -> Literal: ...
def Anti(x):  # pylint:disable=invalid-name
    """Invert a Predicate or Literal effect."""
    if isinstance(x, Predicate):
        return Predicate(
            x.name, x.arity, var_types=x.var_types, is_anti=(not x.is_anti)
        )

    assert isinstance(x, Literal)
    new_predicate = Anti(x.predicate)
    return new_predicate(*x.variables)


@overload
def Effect(x: Predicate) -> Predicate: ...
@overload
def Effect(x: Literal) -> Literal: ...
def Effect(x):  # pylint:disable=invalid-name
    """An effect predicate or literal."""
    assert not x.negated_as_failure
    if isinstance(x, Predicate):
        return Predicate(
            "Effect" + x.name,
            x.arity,
            var_types=x.var_types,
            is_negative=x.is_negative,
            is_anti=x.is_anti,
        )
    assert isinstance(x, Literal)
    new_predicate = Effect(x.predicate)
    return new_predicate(*x.variables)


def effect_to_literal(literal: Literal) -> Literal:
    assert isinstance(literal, Literal)
    assert literal.predicate.name.startswith("Effect")
    non_effect_pred = Predicate(
        literal.predicate.name[len("Effect") :],
        literal.predicate.arity,
        literal.predicate.var_types,
        negated_as_failure=literal.predicate.negated_as_failure,
        is_negative=literal.predicate.is_negative,
        is_anti=literal.predicate.is_anti,
    )
    return non_effect_pred(*literal.variables)


def ground_literal(
    lifted_lit: Literal, assignments: dict[TypedEntity, TypedEntity]
) -> Literal:
    """Given a lifted literal, create a ground
    literal with the assignments mapping vars to
    objects.

    Parameters
    ----------
    lifted_lit : Literal
    assignments : { TypedEntity : TypedEntity }
        Vars to objects.

    Returns
    -------
    ground_lit : Literal
    """
    ground_vars: list[TypedEntity] = []
    for v in lifted_lit.variables:
        arg = assignments[v]
        ground_vars.append(arg)
    return lifted_lit.predicate(*ground_vars)


@overload
def wrap_goal_literal(x: LiteralConjunction) -> LiteralConjunction: ...
@overload
def wrap_goal_literal(x: ForAll) -> ForAll: ...
@overload
def wrap_goal_literal(x: Predicate) -> Predicate: ...
@overload
def wrap_goal_literal(x: Literal) -> Literal: ...
def wrap_goal_literal(x):
    """Append "WANT" to goal literal"""
    if isinstance(x, LiteralConjunction):
        wrapped_body = [wrap_goal_literal(lit) for lit in x.literals]
        return LiteralConjunction(wrapped_body)
    if isinstance(x, ForAll):
        wrapped_body = wrap_goal_literal(x.body)
        return ForAll(wrapped_body, x.variables, is_negative=x.is_negative)
    if isinstance(x, Predicate):
        return Predicate(
            "WANT" + x.name,
            x.arity,
            var_types=x.var_types,
            is_negative=x.is_negative,
            is_anti=x.is_anti,
        )
    assert isinstance(x, Literal)
    new_predicate = wrap_goal_literal(x.predicate)
    return new_predicate(*x.variables)


NoChange: Predicate = Predicate(
    "NOCHANGE", 0
)  # represents no change in a probabilistic effect
