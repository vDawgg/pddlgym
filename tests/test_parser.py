from __future__ import annotations

from pddlgym.parser import PDDLDomainParser, PDDLProblemParser
from pddlgym.structs import Predicate, Type, Anti, LiteralConjunction
from tests.constants import pddl_dir

import unittest


class TestParser(unittest.TestCase):
    def test_parser(self) -> None:
        domain_file = str(pddl_dir / "test_domain.pddl")
        problem_file = str(pddl_dir / "test_domain" / "test_problem.pddl")
        domain = PDDLDomainParser(domain_file)
        assert domain.domain_name is not None
        problem = PDDLProblemParser(
            problem_file,
            domain.domain_name,
            domain.types,
            domain.predicates,
            domain.actions,
        )

        ## Check domain
        type1 = Type("type1")
        type2 = Type("type2")

        # Action predicates
        action_pred = Predicate("actionpred", 1, [type1])

        # Predicates
        pred1 = Predicate("pred1", 1, [type1])
        pred2 = Predicate("pred2", 1, [type2])
        pred3 = Predicate("pred3", 3, [type1, type2, type2])
        assert domain.predicates is not None
        assert set(domain.predicates.values()) == {pred1, pred2, pred3, action_pred}
        assert domain.actions == {action_pred.name}

        # Operators
        assert domain.operators is not None
        assert len(domain.operators) == 1
        operator1 = Predicate("action1", 4, [type1, type1, type2, type2])
        assert operator1 in domain.operators

        operator = domain.operators[operator1.name]
        # Operator parameters
        assert len(operator.params) == 4
        assert operator.params[0] == type1("?a")
        assert operator.params[1] == type1("?b")
        assert operator.params[2] == type2("?c")
        assert operator.params[3] == type2("?d")

        # Operator preconditions (set of Literals)
        assert isinstance(operator.preconds, LiteralConjunction)
        assert len(operator.preconds.literals) == 4
        assert set(operator.preconds.literals) == {
            action_pred("?b"),
            pred1("?b"),
            pred3("?a", "?c", "?d"),
            pred2("?c"),
        }

        # Operator effects (set of Literals)
        assert isinstance(operator.effects, LiteralConjunction)
        assert len(operator.effects.literals) == 2
        assert set(operator.effects.literals) == {
            Anti(pred2("?c")),
            pred3("?b", "?d", "?c"),
        }

        ## Check problem

        # Objects
        assert problem.objects is not None
        assert set(problem.objects) == {
            type1("a1"),
            type1("a2"),
            type1("b1"),
            type1("b2"),
            type1("b3"),
            type2("c1"),
            type2("c2"),
            type2("d1"),
            type2("d2"),
            type2("d3"),
        }

        # Goal
        assert isinstance(problem.goal, LiteralConjunction)
        assert set(problem.goal.literals) == {pred2("c2"), pred3("b1", "c1", "d1")}

        # Init
        assert problem.initial_state == frozenset(
            {pred1("b2"), pred2("c1"), pred3("a1", "c1", "d1"), pred3("a2", "c2", "d2")}
        )


class TestHierarchicalTypes(unittest.TestCase):
    def test_hierarchical_types(self) -> None:
        domain_file = str(pddl_dir / "hierarchical_type_test_domain.pddl")
        problem_file = str(
            pddl_dir
            / "hierarchical_type_test_domain"
            / "hierarchical_type_test_problem.pddl"
        )
        domain = PDDLDomainParser(domain_file)
        assert domain.domain_name is not None
        PDDLProblemParser(
            problem_file,
            domain.domain_name,
            domain.types,
            domain.predicates,
            domain.actions,
        )

        assert domain.types is not None
        assert set(domain.types.keys()) == {
            Type("dog"),
            Type("cat"),
            Type("animal"),
            Type("block"),
            Type("cylinder"),
            Type("jindo"),
            Type("corgi"),
            Type("object"),
            Type("entity"),
        }

        assert domain.type_hierarchy == {
            Type("animal"): {Type("dog"), Type("cat")},
            Type("dog"): {Type("jindo"), Type("corgi")},
            Type("object"): {Type("block"), Type("cylinder")},
            Type("entity"): {Type("object"), Type("animal")},
        }

        assert domain.type_to_parent_types == {
            Type("entity"): {Type("entity")},
            Type("object"): {Type("object"), Type("entity")},
            Type("animal"): {Type("animal"), Type("entity")},
            Type("dog"): {Type("dog"), Type("animal"), Type("entity")},
            Type("cat"): {Type("cat"), Type("animal"), Type("entity")},
            Type("corgi"): {Type("corgi"), Type("dog"), Type("animal"), Type("entity")},
            Type("jindo"): {Type("jindo"), Type("dog"), Type("animal"), Type("entity")},
            Type("block"): {Type("block"), Type("object"), Type("entity")},
            Type("cylinder"): {Type("cylinder"), Type("object"), Type("entity")},
        }

        print("Test passed.")


if __name__ == "__main__":
    unittest.main()
