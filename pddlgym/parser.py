"""PDDL parsing."""

from __future__ import annotations

from pddlgym.structs import (
    Type,
    Predicate,
    Literal,
    LiteralConjunction,
    LiteralDisjunction,
    Not,
    Anti,
    ForAll,
    Exists,
    ProbabilisticEffect,
    TypedEntity,
    ground_literal,
    DerivedPredicate,
    NoChange,
)

from typing import Dict, FrozenSet, Iterable, List, Optional, Set, Union, cast

import re


FAST_DOWNWARD_STR = """
(define (problem {problem}) (:domain {domain})
  (:objects
        {objects}
  )
  (:init \n\t{init_state}
  )
  (:goal {goal})
)
"""

PROBLEM_STR = """
(define (problem {problem}) (:domain {domain})
  (:objects
        {objects}
  )
  (:goal {goal})
  (:init \n\t{init_state}
))
"""


class Operator:
    """Class to hold an operator."""

    def __init__(
        self,
        name: str,
        params: List[TypedEntity],
        preconds: Union[Literal, LiteralConjunction],
        effects: Union[Literal, LiteralConjunction],
    ) -> None:
        self.name: str = name
        self.params: List[TypedEntity] = params
        self.preconds: Union[Literal, LiteralConjunction] = preconds
        self.effects: Union[Literal, LiteralConjunction] = effects

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        s = self.name + "(" + ",".join(map(str, self.params)) + "): "
        if isinstance(self.preconds, Literal):
            s += str(self.preconds)
        else:
            s += " & ".join(map(str, self.preconds.literals))
        s += " => "
        if isinstance(self.effects, Literal):
            s += str(self.effects)
        else:
            s += " & ".join(map(str, self.effects.literals))
        return s

    def pddl_str(self) -> str:
        param_strs = [str(param).replace(":", " - ") for param in self.params]
        s = "\n\n\t(:action {}".format(self.name)
        s += "\n\t\t:parameters ({})".format(" ".join(param_strs))
        preconds_pddl_str = self._create_preconds_pddl_str(self.preconds)
        s += "\n\t\t:precondition (and {})".format(preconds_pddl_str)
        indented_effs = self.effects.pddl_str().replace("\n", "\n\t\t")
        s += "\n\t\t:effect {}".format(indented_effs)
        s += "\n\t)"
        return s

    def _create_preconds_pddl_str(
        self, preconds: Union[Literal, LiteralConjunction]
    ) -> str:
        all_params = set()
        precond_strs = []
        if isinstance(preconds, Literal):
            preconds = LiteralConjunction([preconds])
        for term in preconds.literals:
            params = set(map(str, term.variables))
            if hasattr(term, "negated_as_failure") and term.negated_as_failure:
                universally_quantified_vars = list(sorted(params - all_params))
                precond = ""
                for var in universally_quantified_vars:
                    precond += "(forall ({}) ".format(var.replace(":", " - "))
                precond += "(or "
                for var in universally_quantified_vars:
                    var_cleaned = "?" + var[: var.find(":")]
                    for param in list(sorted(all_params)):
                        param_cleaned = "?" + param[: param.find(":")]
                        precond += "(not (Different {} {})) ".format(
                            param_cleaned, var_cleaned
                        )
                precond += "(not {}))".format(term.positive.pddl_str())
                for var in universally_quantified_vars:
                    precond += ")"
                precond_strs.append(precond)
            else:
                all_params.update(params)
                precond_strs.append(term.pddl_str())

        return "\n\t\t\t".join(precond_strs)


class PDDLParser:
    """PDDL parsing class."""

    types: dict[str, Type]
    predicates: dict[str, Predicate]
    uses_typing: bool

    def _parse_into_literal(
        self,
        string: str,
        params: Union[List[TypedEntity], Dict[str, Type]],
        is_effect: bool = False,
    ) -> Union[
        Literal,
        LiteralConjunction,
        LiteralDisjunction,
        ForAll,
        Exists,
        ProbabilisticEffect,
    ]:
        """Parse the given string (representing either preconditions or effects)
        into a literal. Check against params to make sure typing is correct.
        """
        assert string[0] == "("
        assert string[-1] == ")"
        if string.startswith("(and") and string[4] in (" ", "\n", "(", ")"):
            clauses = self._find_all_balanced_expressions(string[4:-1].strip())
            return LiteralConjunction(
                cast(
                    List[Literal],
                    [
                        self._parse_into_literal(clause, params, is_effect=is_effect)
                        for clause in clauses
                    ],
                )
            )
        if string.startswith("(or") and string[3] in (" ", "\n", "(", ")"):
            clauses = self._find_all_balanced_expressions(string[3:-1].strip())
            return LiteralDisjunction(
                cast(
                    List[Literal],
                    [
                        self._parse_into_literal(clause, params, is_effect=is_effect)
                        for clause in clauses
                    ],
                )
            )
        if string.startswith("(imply") and string[6] in (" ", "\n", "("):
            clauses = self._find_all_balanced_expressions(string[6:-1].strip())
            assert len(clauses) == 2
            assert not is_effect, "Imply is only allowed in preconditions"
            premise = self._parse_into_literal(clauses[0], params, is_effect=is_effect)
            implic = self._parse_into_literal(clauses[1], params, is_effect=is_effect)
            assert isinstance(premise, Literal)
            assert isinstance(implic, Literal)
            return LiteralDisjunction([Not(premise), implic])
        if string.startswith("(forall") and string[7] in (" ", "\n", "("):
            new_binding, clause = self._find_all_balanced_expressions(
                string[7:-1].strip()
            )
            new_name, new_type_name = new_binding.strip()[1:-1].split("-", 1)
            new_name = new_name.strip()
            new_type_name = new_type_name.strip()
            assert new_name not in params, "ForAll variable {} already exists".format(
                new_name
            )
            new_entity_type = self.types[new_type_name]
            new_entity = TypedEntity(new_name, new_entity_type)
            if isinstance(params, list):
                new_params = params + [new_entity]
            else:
                new_params = params.copy()
                new_params[new_name] = self.types[new_type_name]
            result = ForAll(
                self._parse_into_literal(clause, new_params, is_effect=is_effect),
                new_entity,
            )
            return result
        if string.startswith("(exists") and string[7] in (" ", "\n", "("):
            new_binding, clause = self._find_all_balanced_expressions(
                string[7:-1].strip()
            )
            if new_binding[1:-1] == "":
                body = self._parse_into_literal(clause, params, is_effect=is_effect)
                return body
            variables = self.parse_objects(
                new_binding[1:-1], self.types, uses_typing=self.uses_typing
            )
            if isinstance(params, list):
                for v in variables:
                    params.append(v.var_type(v.name))
            else:
                for v in variables:
                    params[v.name] = v.var_type
            body = self._parse_into_literal(clause, params, is_effect=is_effect)
            result = Exists(variables, body)
            if isinstance(params, list):
                for v in variables:
                    params.remove(v)
            else:
                for v in variables:
                    del params[v.name]
            return result
        if string.startswith("(probabilistic") and string[14] in (" ", "\n", "("):
            assert is_effect, "We only support probabilistic effects"
            lits = []
            probs = []
            expr = string[14:-1].strip()
            for match in re.finditer(r"(\d*\.\d+)", expr):
                prob = float(match.group())
                subexpr = self._find_balanced_expression(expr[match.end() :].strip(), 0)
                lit = self._parse_into_literal(subexpr, params, is_effect=is_effect)
                lits.append(lit)
                probs.append(prob)
            return ProbabilisticEffect(cast(List[Literal], lits), probs)
        if string.startswith("(not") and string[4] in (" ", "\n", "("):
            clause = string[4:-1].strip()
            if is_effect:
                inner = self._parse_into_literal(clause, params, is_effect=is_effect)
                assert isinstance(inner, Literal)
                return Anti(inner)
            else:
                inner = self._parse_into_literal(clause, params, is_effect=is_effect)
                assert isinstance(inner, Literal)
                return Not(inner)
        parts = string[1:-1].split()
        pred, args = parts[0], parts[1:]
        typed_args: List[TypedEntity] = []
        assert pred in self.predicates, "Predicate {} is not defined".format(pred)
        assert self.predicates[pred].arity == len(args), pred
        for i, arg in enumerate(args):
            if arg not in params:
                raise Exception("Argument {} not in params {}".format(arg, params))
            assert arg in params, "Argument {} is not in the params".format(arg)
            if isinstance(params, dict):
                typed_arg = TypedEntity(arg, params[arg])
            else:
                typed_arg = next(p for p in params if p.name == arg)
            typed_args.append(typed_arg)
        return self.predicates[pred](*typed_args)

    @staticmethod
    def parse_objects(
        objects_str: str, types: Dict[str, Type], uses_typing: bool = False
    ) -> List[TypedEntity]:
        if uses_typing:
            objects: List[str] = []
            remaining_str = objects_str
            while True:
                try:
                    obj, remaining_str = re.split(r"\s-\s|\n-\s", remaining_str, 1)
                except ValueError:
                    break
                if " " in remaining_str:
                    object_type, remaining_str = re.split(
                        r"[\s]+|[\n]+", remaining_str, 1
                    )
                else:
                    object_type = remaining_str
                    remaining_str = ""
                objects.append(obj + " - " + object_type)
        else:
            objects = objects_str.split()
        obj_names = []
        obj_type_names = []
        for obj in objects:
            if uses_typing:
                obj_name, obj_type_name = obj.strip().split(" - ")
                obj_name = obj_name.strip()
                obj_type_name = obj_type_name.strip()
                if len(obj_name.split()) > 1:
                    for single_obj_name in obj_name.split():
                        obj_names.append(single_obj_name.strip())
                        obj_type_names.append(obj_type_name)
                else:
                    obj_names.append(obj_name)
                    obj_type_names.append(obj_type_name)
            else:
                obj_name = obj.strip()
                if " - " in obj_name:
                    obj_name, temp = obj_name.split(" - ")
                    obj_name = obj_name.strip()
                    assert temp == "default"
                obj_type_name = "default"
                obj_names.append(obj_name)
                obj_type_names.append(obj_type_name)
        to_return = set()
        for obj_name, obj_type_name in zip(obj_names, obj_type_names):
            if obj_type_name not in types:
                print(
                    "Warning: type not declared for object {}, type {}".format(
                        obj_name, obj_type_name
                    )
                )
                obj_type = Type(obj_type_name)
            else:
                obj_type = types[obj_type_name]
            to_return.add(TypedEntity(obj_name, obj_type))
        return sorted(to_return)

    def _purge_comments(self, pddl_str: str) -> str:
        while True:
            match = re.search(r";(.*)\n", pddl_str)
            if match is None:
                return pddl_str
            start, end = match.start(), match.end()
            pddl_str = pddl_str[:start] + pddl_str[end - 1 :]

    @staticmethod
    def _find_balanced_expression(string: str, index: int) -> str:
        """Find balanced expression in string starting from given index."""
        assert string[index] == "("
        start_index = index
        balance = 1
        while balance != 0:
            index += 1
            symbol = string[index]
            if symbol == "(":
                balance += 1
            elif symbol == ")":
                balance -= 1
        return string[start_index : index + 1]

    @staticmethod
    def _find_all_balanced_expressions(string: str) -> List[str]:
        """Return a list of all balanced expressions in a string,
        starting from the beginning.
        """
        if not string:
            return []
        assert string[0] == "("
        assert string[-1] == ")"
        exprs = []
        index = 0
        start_index = index
        balance = 1
        while index < len(string) - 1:
            index += 1
            if balance == 0:
                exprs.append(string[start_index:index])
                while True:
                    if string[index] == "(":
                        break
                    index += 1
                start_index = index
                balance = 1
                continue
            symbol = string[index]
            if symbol == "(":
                balance += 1
            elif symbol == ")":
                balance -= 1
        assert balance == 0
        exprs.append(string[start_index : index + 1])
        return exprs


class PDDLDomain:
    """A PDDL domain."""

    def __init__(
        self,
        domain_name: Optional[str] = None,
        types: Optional[Dict[str, Type]] = None,
        type_hierarchy: dict[Type, set[Type]] | None = None,
        predicates: Optional[Dict[str, Predicate]] = None,
        operators: Optional[Dict[str, Operator]] = None,
        actions: set[str] | None = None,
        constants: Optional[List[TypedEntity]] = None,
        operators_as_actions: bool = False,
        is_probabilistic: bool = False,
    ) -> None:
        self.domain_name: Optional[str] = domain_name
        self.types: Dict[str, Type] = types or {}
        self.type_hierarchy: dict[Type, set[Type]] = type_hierarchy or {}
        self.predicates: Dict[str, Predicate] = predicates or {}
        self.operators: Dict[str, Operator] = operators or {}
        self.actions: set[str] = actions or set()
        self.constants: List[TypedEntity] = constants or []
        self.operators_as_actions: bool = operators_as_actions
        self.is_probabilistic: bool = is_probabilistic

    @property
    def type_to_parent_types(self) -> Dict[Type, Set[Type]]:
        """For convenience, create map of subtype to all parent types"""
        return self._organize_parent_types()

    def determinize(self) -> None:
        """Determinize this operator by assuming max-probability effects."""
        assert self.is_probabilistic
        for op in self.operators.values():
            assert isinstance(op.effects, LiteralConjunction)
            toremove = set()
            for i, lit in enumerate(op.effects.literals):
                if isinstance(lit, ProbabilisticEffect):
                    chosen_effect = lit.max()
                    if chosen_effect == NoChange():
                        toremove.add(lit)
                    else:
                        op.effects.literals[i] = chosen_effect
            for rem in toremove:
                op.effects.literals.remove(rem)

    def _organize_parent_types(self) -> Dict[Type, Set[Type]]:
        """Create dict of type -> parent types from type hierarchy"""
        type_to_parent_types: Dict[Type, Set[Type]] = {
            t: {t} for t in self.types.values()
        }
        for t in self.types.values():
            parent_types = self._get_parent_types(t)
            type_to_parent_types[t].update(parent_types)
        return type_to_parent_types

    def _get_parent_types(self, t: Type) -> Set[Type]:
        """Helper for organize parent types"""
        parent_types: Set[Type] = set()
        for super_type, sub_types in self.type_hierarchy.items():
            if t in sub_types:
                parent_types.add(super_type)
                parent_types.update(self._get_parent_types(super_type))
        return parent_types

    def to_string(self) -> str:
        """Create PDDL string"""
        predicates = "\n\t".join([lit.pddl_str() for lit in self.predicates.values()])
        operators = "\n\t".join([op.pddl_str() for op in self.operators.values()])
        if self.constants:
            constants_str = "\n\t".join(
                list(sorted(map(lambda o: str(o).replace(":", " - "), self.constants)))
            )
            constants = f"\n  (:constants {constants_str})\n"
        else:
            constants = ""
        requirements = ":typing"
        if "=" in self.predicates:
            requirements += " :equality"

        domain_str = """
(define (domain {})
  (:requirements {})
  (:types {})
  {}
  (:predicates {}
  )
  ; (:actions {})

  {}

  {}

)
        """.format(
            self.domain_name,
            requirements,
            self._types_pddl_str(),
            constants,
            predicates,
            " ".join(map(str, self.actions)),
            operators,
            self._derived_preds_pddl_str(),
        )
        return domain_str

    def write(self, fname: str) -> None:
        """Write the domain PDDL string to a file."""
        domain_str = self.to_string()

        with open(fname, "w") as f:
            f.write(domain_str)

    def _types_pddl_str(self) -> str:
        if self.type_hierarchy:
            return "\n".join(
                [
                    "{} - {}".format(" ".join(self.type_hierarchy[k]), k)
                    for k in self.type_hierarchy
                ]
            )
        else:
            return " ".join(self.types)

    def _derived_preds_pddl_str(self) -> str:
        mystr = ""
        for pred in self.predicates.values():
            if pred.is_derived:
                assert isinstance(pred, DerivedPredicate)
                mystr += "{}\n\n".format(pred.derived_pddl_str())
        return mystr


class PDDLDomainParser(PDDLParser, PDDLDomain):
    """PDDL domain parsing class."""

    def __init__(
        self,
        domain_fname: str,
        expect_action_preds: bool = True,
        operators_as_actions: bool = False,
    ) -> None:
        PDDLDomain.__init__(self, operators_as_actions=operators_as_actions)

        self.domain_fname: str = domain_fname

        with open(domain_fname, "r") as f:
            self.domain: str = f.read().lower()

        self.is_probabilistic: bool = "probabilistic" in self.domain

        if expect_action_preds:
            self.actions: set = self._parse_actions()

        self.domain = self._purge_comments(self.domain)
        assert ";" not in self.domain

        self._parse_domain()

        if operators_as_actions:
            assert not expect_action_preds
            self.actions = self._create_actions_from_operators()
        elif not expect_action_preds:
            self.actions = set()

    def _parse_actions(self) -> Set[str]:
        match = re.search(r"\(:actions", self.domain)
        assert match is not None
        start_ind = match.start()
        actions = self._find_balanced_expression(self.domain, start_ind)
        actions = actions[9:-1].strip()
        return set(actions.split())

    def _create_actions_from_operators(self) -> Set[Predicate]:
        actions: Set[Predicate] = set()
        for name, operator in self.operators.items():
            types = [p.var_type for p in operator.params]
            action = Predicate(name, len(types), types)
            assert name not in self.predicates, (
                "Cannot have predicate with same name as operator"
            )
            self.predicates[name] = action
            actions.add(action)
        return actions

    def _parse_domain(self) -> None:
        patt = r"\(domain(.*?)\)"
        match = re.search(patt, self.domain)
        assert match is not None
        self.domain_name = match.groups()[0].strip()
        self._parse_domain_types()
        self._parse_domain_predicates()
        self._parse_domain_derived_predicates()
        self._parse_constants()
        self._parse_domain_operators()

    def _parse_domain_types(self) -> None:
        match = re.search(r"\(:types", self.domain)
        if not match:
            self.types = {"default": Type("default")}
            self.type_hierarchy = {}
            self.uses_typing = False
            return
        self.uses_typing = True
        start_ind = match.start()
        types = self._find_balanced_expression(self.domain, start_ind)
        if " - " not in types:
            types = types[7:-1].split()
            self.types = {type_name: Type(type_name) for type_name in types}
            self.type_hierarchy = {}
        else:
            self.types = {}
            self.type_hierarchy = {}
            remaining_type_str = types[7:-1]
            while " - " in remaining_type_str:
                dash_index = remaining_type_str.index(" - ")
                s = remaining_type_str[dash_index:]
                super_start_index = dash_index + len(s) - len(s.lstrip()) + 2
                s = remaining_type_str[super_start_index:]
                try:
                    end_index_offset = min(s.index(" "), s.index("\n"))
                except ValueError:
                    end_index_offset = len(s)
                super_end_index = super_start_index + end_index_offset
                super_type_name = remaining_type_str[super_start_index:super_end_index]
                sub_type_names = remaining_type_str[:dash_index].split()
                for new_type in sub_type_names + [super_type_name]:
                    if new_type not in self.types:
                        self.types[new_type] = Type(new_type)
                super_type = self.types[super_type_name]
                if super_type in self.type_hierarchy:
                    self.type_hierarchy[super_type].update(
                        {self.types[t] for t in sub_type_names}
                    )
                else:
                    self.type_hierarchy[super_type] = {
                        self.types[t] for t in sub_type_names
                    }
                remaining_type_str = remaining_type_str[super_end_index:]
            assert len(remaining_type_str.strip()) == 0, (
                "Cannot mix hierarchical and non-hierarchical types"
            )

    def _parse_constants(self) -> None:
        if ":constants" not in self.domain:
            self.constants = []
            return
        match = re.search(r"\(:constants", self.domain)
        assert match is not None
        start_ind = match.start()
        constants = self._find_balanced_expression(self.domain, start_ind)
        constants = constants[11:-1].strip()
        if constants == "":
            self.constants = []
        else:
            self.constants = PDDLProblemParser.parse_objects(
                constants, self.types, uses_typing=self.uses_typing
            )

    def _parse_domain_predicates(self) -> None:
        match = re.search(r"\(:predicates", self.domain)
        assert match is not None
        start_ind = match.start()
        predicates = self._find_balanced_expression(self.domain, start_ind)
        predicates = predicates[12:-1].strip()
        predicates = self._find_all_balanced_expressions(predicates)
        self.predicates = {}
        for pred in predicates:
            pred = pred.strip()[1:-1].split("?")
            pred_name = pred[0].strip()
            arg_types = []
            for arg in pred[1:]:
                if " - " in arg:
                    assert arg_types is not None, (
                        "Mixing of typed and untyped args not allowed"
                    )
                    assert self.uses_typing
                    arg_type = self.types[arg.strip().split("-", 1)[1].strip()]
                    arg_types.append(arg_type)
                else:
                    assert not self.uses_typing
                    arg_types.append(self.types["default"])
            self.predicates[pred_name] = Predicate(pred_name, len(pred[1:]), arg_types)
        if "=" in self.domain:
            self.predicates["="] = Predicate("=", 2)

    def _parse_domain_derived_predicates(self) -> None:
        for match in re.finditer(r"\(:derived", self.domain):
            derived_pred = self._find_balanced_expression(self.domain, match.start())
            derived_pred = derived_pred[9:-1].strip()
            head, body = self._find_all_balanced_expressions(derived_pred)
            head = head.strip().strip("(").strip(")")
            name = head.split()[0]
            assert name in self.predicates
            params = head.split("?")[1:]
            var_types = self.predicates[name].var_types
            assert var_types is not None
            assert len(params) == len(var_types)
            params = [
                param_type("?" + param.strip())
                for param, param_type in zip(params, var_types)
            ]
            del self.predicates[name]
            derived_pred = DerivedPredicate(name, len(params), var_types)
            self.predicates[name] = derived_pred
            body = self._parse_into_literal(body, params)
            param_names = [p.name for p in params]
            derived_pred.setup(param_names, body)

    def _parse_domain_operators(self) -> None:
        matches = re.finditer(r"\(:action", self.domain)
        self.operators = {}
        for match in matches:
            start_ind = match.start()
            op = self._find_balanced_expression(self.domain, start_ind).strip()
            patt = r"\(:action(.*):parameters(.*):precondition(.*):effect(.*)\)"
            op_match = re.match(patt, op, re.DOTALL)
            assert op_match is not None
            op_name, params, preconds, effects = op_match.groups()
            op_name = op_name.strip()
            params = params.strip()[1:-1].split("?")
            if self.uses_typing:
                params = [
                    (
                        param.strip().split("-", 1)[0].strip(),
                        param.strip().split("-", 1)[1].strip(),
                    )
                    for param in params[1:]
                ]
                params = [self.types[v]("?" + k) for k, v in params]
            else:
                params = [param.strip() for param in params[1:]]
                params = [self.types["default"]("?" + k) for k in params]
            preconds = self._parse_into_literal(
                preconds.strip(), params + self.constants
            )
            effects = self._parse_into_literal(
                effects.strip(), params + self.constants, is_effect=True
            )
            assert isinstance(preconds, (Literal, LiteralConjunction))
            assert isinstance(effects, (Literal, LiteralConjunction))
            self.operators[op_name] = Operator(op_name, params, preconds, effects)


class PDDLProblemParser(PDDLParser):
    """PDDL problem parsing class."""

    def __init__(
        self,
        problem_fname: str,
        domain_name: str,
        types: Dict[str, Type],
        predicates: Dict[str, Predicate],
        action_names: set[str],
        constants: list[TypedEntity] | None = None,
    ) -> None:
        self.problem_fname: str = problem_fname
        self.domain_name: str = domain_name
        self.types: Dict[str, Type] = types
        self.predicates: Dict[str, Predicate] = predicates
        self.action_names: Set[str] = action_names
        self.uses_typing: bool = "default" not in self.types
        self.constants: List[TypedEntity] = constants or []

        self.problem_name: Optional[str] = None
        self.objects: Optional[List[TypedEntity]] = None
        self.initial_state: Optional[FrozenSet[Literal]] = None
        self.goal: Optional[Literal] = None

        with open(problem_fname, "r") as f:
            self.problem: str = f.read().lower()
        self.problem = self._purge_comments(self.problem)
        assert ";" not in self.problem

        self._parse_problem()

    def _parse_problem(self) -> None:
        patt = r"\(problem(.*?)\)"
        problem_match = re.search(patt, self.problem)
        assert problem_match is not None
        self.problem_name = problem_match.groups()[0].strip()
        patt = r"\(:domain(.*?)\)"
        domain_match = re.search(patt, self.problem)
        assert domain_match is not None
        domain_name = domain_match.groups()[0].strip()
        assert domain_name == self.domain_name, (
            "Problem file doesn't match the domain file!"
        )
        self._parse_problem_objects()
        self._parse_problem_initial_state()
        self._parse_problem_goal()

    def _parse_problem_objects(self) -> None:
        match = re.search(r"\(:objects", self.problem)
        assert match is not None
        start_ind = match.start()
        objects = self._find_balanced_expression(self.problem, start_ind)
        objects = objects[9:-1].strip()
        if objects == "":
            self.objects = []
        else:
            self.objects = self.parse_objects(
                objects, self.types, uses_typing=self.uses_typing
            )
        self.objects += self.constants

    def _parse_problem_initial_state(self) -> None:
        match = re.search(r"\(:init", self.problem)
        assert match is not None
        start_ind = match.start()
        init = self._find_balanced_expression(self.problem, start_ind)
        fluents = self._find_all_balanced_expressions(init[6:-1].strip())
        initial_lits: set[Literal] = set()
        assert self.objects is not None
        params = {obj.name: obj.var_type for obj in self.objects}
        for fluent in fluents:
            lit = self._parse_into_literal(fluent, params)
            assert isinstance(lit, Literal)
            if lit.predicate.name in self.action_names:
                continue
            initial_lits.add(lit)
        if "=" in self.predicates:
            eq = self.predicates["="]
            for obj in self.objects:
                initial_lits.add(eq(obj, obj))
        self.initial_state = frozenset(initial_lits)

    def _parse_problem_goal(self) -> None:
        match = re.search(r"\(:goal", self.problem)
        assert match is not None
        start_ind = match.start()
        goal = self._find_balanced_expression(self.problem, start_ind)
        goal = goal[6:-1].strip()
        assert self.objects is not None
        params = {obj.name: obj.var_type for obj in self.objects}
        goal_lit = self._parse_into_literal(goal, params)
        assert isinstance(goal_lit, Literal)
        self.goal = goal_lit

    @staticmethod
    def pddl_string(
        objects: Iterable[TypedEntity],
        initial_state: frozenset[Literal] | set[Literal],
        problem_name: str,
        domain_name: str,
        goal: Literal | LiteralConjunction,
        fast_downward_order: bool = False,
    ) -> str:
        """Get the problem PDDL string for a given state."""
        objects_typed = "\n\t".join(
            list(sorted(map(lambda o: str(o).replace(":", " - "), objects)))
        )
        init_state = "\n\t".join(
            [
                lit.pddl_str()
                for lit in sorted(initial_state)
                if not lit.predicate.is_derived and lit.predicate.name != "="
            ]
        )

        problem_str = FAST_DOWNWARD_STR if fast_downward_order else PROBLEM_STR
        return problem_str.format(
            problem=problem_name,
            domain=domain_name,
            objects=objects_typed,
            init_state=init_state,
            goal=goal.pddl_str(),
        )

    @staticmethod
    def create_pddl_file(
        file_or_filepath,
        objects: Iterable[TypedEntity],
        initial_state: frozenset[Literal] | set[Literal],
        problem_name: str,
        domain_name: str,
        goal: Literal | LiteralConjunction,
        fast_downward_order: bool = False,
    ) -> None:
        """Write the problem PDDL string for a given state into a file."""
        problem_str = PDDLProblemParser.pddl_string(
            objects=objects,
            initial_state=initial_state,
            problem_name=problem_name,
            domain_name=domain_name,
            goal=goal,
            fast_downward_order=fast_downward_order,
        )

        try:
            file_or_filepath.write(problem_str)
        except AttributeError:
            with open(file_or_filepath, "w") as f:
                f.write(problem_str)

    def write(
        self,
        file_or_filepath,
        objects: Optional[Iterable[TypedEntity]] = None,
        initial_state: Optional[frozenset[Literal] | set[Literal]] = None,
        problem_name: Optional[str] = None,
        domain_name: Optional[str] = None,
        goal: Optional[Literal] = None,
        fast_downward_order: bool = False,
    ) -> None:
        """Write the problem PDDL string for a given state."""
        if objects is None:
            assert self.objects is not None
            objects = self.objects
        if initial_state is None:
            assert self.initial_state is not None
            initial_state = self.initial_state
        if problem_name is None:
            assert self.problem_name is not None
            problem_name = self.problem_name
        if domain_name is None:
            assert self.domain_name is not None
            domain_name = self.domain_name
        if goal is None:
            assert self.goal is not None
            goal = self.goal

        return PDDLProblemParser.create_pddl_file(
            file_or_filepath,
            objects=objects,
            initial_state=initial_state,
            problem_name=problem_name,
            domain_name=domain_name,
            goal=goal,
            fast_downward_order=fast_downward_order,
        )


def parse_plan_step(
    plan_step: str,
    operators: List[Operator],
    action_predicates: set[Predicate] | list[Predicate],
    objects: List[TypedEntity],
    operators_as_actions: bool = False,
) -> Literal:
    plan_step_split = plan_step.split()

    if operators_as_actions:
        action_predicate = [
            a for a in action_predicates if a.name.lower() == plan_step_split[0].lower()
        ][0]
        object_names = plan_step_split[1:]
        args = []
        for name in object_names:
            matches = [o for o in objects if o.name == name]
            assert len(matches) == 1
            args.append(matches[0])
        return action_predicate(*args)

    operator = None
    for op in operators:
        if op.name.lower() == plan_step_split[0]:
            operator = op
            break
    assert operator is not None, "Unknown operator '{}'".format(plan_step_split[0])

    assert len(plan_step_split) == len(operator.params) + 1
    object_names = plan_step_split[1:]
    args = []
    for name in object_names:
        matches = [o for o in objects if o.name == name]
        assert len(matches) == 1
        args.append(matches[0])
    assignments = dict(zip(operator.params, args))

    assert isinstance(operator.preconds, LiteralConjunction)
    for cond in operator.preconds.literals:
        if cond.predicate in action_predicates:
            ground_action = ground_literal(cond, assignments)
            return ground_action

    raise Exception("Unrecognized plan step: `{}`".format(str(plan_step)))
