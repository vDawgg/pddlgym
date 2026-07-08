from __future__ import annotations

from nl_pddlgym.core import PDDLEnv, InvalidAction
from nl_pddlgym.structs import (
    Predicate,
    DerivedPredicate,
    Type,
    LiteralConjunction,
    ForAll,
)

from tests.constants import pddl_dir

import unittest


class TestPDDLEnv(unittest.TestCase):
    def test_pddlenv(self) -> None:
        domain_file = str(pddl_dir / "test_domain.pddl")
        problem_dir = str(pddl_dir / "test_domain")

        env = PDDLEnv(
            domain_file,
            problem_dir,
            raise_error_on_invalid_action=True,
            dynamic_action_space=True,
        )
        env2 = PDDLEnv(
            domain_file,
            problem_dir,
            raise_error_on_invalid_action=True,
            dynamic_action_space=False,
        )

        type1 = Type("type1")
        type2 = Type("type2")
        pred1 = Predicate("pred1", 1, [type1])
        pred2 = Predicate("pred2", 1, [type2])
        pred3 = Predicate("pred3", 3, [type1, type2, type2])
        action_pred = Predicate("actionpred", 1, [type1])

        obs, _ = env.reset()

        assert obs.literals == frozenset(
            {pred1("b2"), pred2("c1"), pred3("a1", "c1", "d1"), pred3("a2", "c2", "d2")}
        )

        # Invalid action
        action = action_pred("b1")

        try:
            env.step(action)
            assert False, "Action was supposed to be invalid"
        except InvalidAction:
            pass

        assert action not in env.action_space.all_ground_literals(obs), (
            "Dynamic action space not working"
        )
        env2.reset()
        assert action in env2.action_space.all_ground_literals(obs), (
            "Dynamic action space not working"
        )

        # Valid args
        action = action_pred("b2")

        obs, _, _, _, _ = env.step(action)

        assert obs.literals == frozenset(
            {
                pred1("b2"),
                pred3("b2", "d1", "c1"),
                pred3("a1", "c1", "d1"),
                pred3("a2", "c2", "d2"),
            }
        )

        assert isinstance(obs.goal, LiteralConjunction)
        assert set(obs.goal.literals) == {pred2("c2"), pred3("b1", "c1", "d1")}

    def test_pddlenv_hierarchical_types(self) -> None:
        domain_file = str(pddl_dir / "hierarchical_type_test_domain.pddl")
        problem_dir = str(pddl_dir / "hierarchical_type_test_domain")

        env = PDDLEnv(domain_file, problem_dir)
        obs, _ = env.reset()

        ispresent = Predicate("ispresent", 1, [Type("entity")])
        islight = Predicate("islight", 1, [Type("object")])
        isfurry = Predicate("isfurry", 1, [Type("animal")])
        ishappy = Predicate("ishappy", 1, [Type("animal")])
        pet = Predicate("pet", 1, [Type("animal")])

        nomsy = Type("jindo")("nomsy")
        rover = Type("corgi")("rover")
        rene = Type("cat")("rene")
        block1 = Type("block")("block1")
        block2 = Type("block")("block2")
        cylinder1 = Type("cylinder")("cylinder1")

        assert obs.literals == frozenset(
            {
                ispresent(nomsy),
                ispresent(rover),
                ispresent(rene),
                ispresent(block1),
                ispresent(block2),
                ispresent(cylinder1),
                islight(block1),
                islight(cylinder1),
                isfurry(nomsy),
            }
        )

        obs, _, _, _, _ = env.step(pet("block1"))

        assert obs.literals == frozenset(
            {
                ispresent(nomsy),
                ispresent(rover),
                ispresent(rene),
                ispresent(block1),
                ispresent(block2),
                ispresent(cylinder1),
                islight(block1),
                islight(cylinder1),
                isfurry(nomsy),
            }
        )

        obs, _, _, _, _ = env.step(pet(nomsy))

        assert obs.literals == frozenset(
            {
                ispresent(nomsy),
                ispresent(rover),
                ispresent(rene),
                ispresent(block1),
                ispresent(block2),
                ispresent(cylinder1),
                islight(block1),
                islight(cylinder1),
                isfurry(nomsy),
                ishappy(nomsy),
            }
        )

    def test_derived_predicates(self) -> None:
        domain_file = str(pddl_dir / "derivedblocks.pddl")
        problem_dir = str(pddl_dir / "derivedblocks")

        env = PDDLEnv(domain_file, problem_dir)
        obs, _ = env.reset()

        on_loc = Predicate("on_loc", 2, [Type("obj"), Type("loc")])
        on_obj = Predicate("on_obj", 2, [Type("obj"), Type("obj")])
        in_gripper = Predicate("in_gripper", 2, [Type("obj"), Type("robot")])

        # derived predicates
        obj_clear = DerivedPredicate(name="obj_clear", arity=1, var_types=[Type("obj")])
        obj_clear.setup(
            param_names=["?v_1"],
            body=ForAll(
                variables=[Type("obj")("?o")],
                body=on_obj("?o", "?v_1").negative,
            ),
        )
        gripper_empty = DerivedPredicate(
            name="gripper_empty", arity=1, var_types=[Type("robot")]
        )
        gripper_empty.setup(
            param_names=["?v_1"],
            body=ForAll(
                variables=[Type("obj")("?o")],
                body=in_gripper("?o", "?v_1").negative,
            ),
        )

        block1 = Type("obj")("block1")
        block2 = Type("obj")("block2")
        gripper = Type("robot")("gripper")
        table = Type("loc")("table")

        assert obs.literals == frozenset(
            {
                on_loc(block2, table),
                on_obj(block1, block2),
                gripper_empty(gripper),
                obj_clear(block1),
            }
        )

    def test_get_all_possible_transitions(self) -> None:
        domain_file = str(pddl_dir / "test_probabilistic_domain.pddl")
        problem_dir = str(pddl_dir / "test_probabilistic_domain")

        env = PDDLEnv(
            domain_file,
            problem_dir,
            raise_error_on_invalid_action=True,
            dynamic_action_space=True,
        )

        obs, _ = env.reset()
        action = env.action_space.all_ground_literals(obs).pop()
        transitions = env.get_all_possible_transitions(action)

        transition_list = list(transitions)
        assert len(transition_list) == 2
        state1, _, _, _ = transition_list[0]
        state2, _, _, _ = transition_list[1]

        type1 = Type("type1")
        type2 = Type("type2")
        pred1 = Predicate("pred1", 1, [type1])
        pred2 = Predicate("pred2", 1, [type2])
        pred3 = Predicate("pred3", 3, [type1, type2, type2])

        state1, state2 = (
            (state1, state2) if pred2("c1") in state2.literals else (state2, state1)
        )

        assert state1.literals == frozenset(
            {
                pred1("b2"),
                pred3("a1", "c1", "d1"),
                pred3("a2", "c2", "d2"),
                pred3("b2", "d1", "c1"),
            }
        )
        assert state2.literals == frozenset(
            {
                pred1("b2"),
                pred2("c1"),
                pred3("a1", "c1", "d1"),
                pred3("a2", "c2", "d2"),
                pred3("b2", "d1", "c1"),
            }
        )

        # Now test again with return_probs=True.
        transitions = env.get_all_possible_transitions(action, return_probs=True)

        transition_list = list(transitions)
        assert len(transition_list) == 2
        assert (
            abs(transition_list[0][1] - 0.3) < 1e-5
            or abs(transition_list[0][1] - 0.7) < 1e-5
        )
        assert (
            abs(transition_list[1][1] - 0.3) < 1e-5
            or abs(transition_list[1][1] - 0.7) < 1e-5
        )
        assert abs(transition_list[0][1] - transition_list[1][1]) > 0.3
        state1, _, _, _ = transition_list[0][0]
        state2, _, _, _ = transition_list[1][0]

        type1 = Type("type1")
        type2 = Type("type2")
        pred1 = Predicate("pred1", 1, [type1])
        pred2 = Predicate("pred2", 1, [type2])
        pred3 = Predicate("pred3", 3, [type1, type2, type2])

        state1, state2 = (
            (state1, state2) if pred2("c1") in state2.literals else (state2, state1)
        )

        assert state1.literals == frozenset(
            {
                pred1("b2"),
                pred3("a1", "c1", "d1"),
                pred3("a2", "c2", "d2"),
                pred3("b2", "d1", "c1"),
            }
        )
        assert state2.literals == frozenset(
            {
                pred1("b2"),
                pred2("c1"),
                pred3("a1", "c1", "d1"),
                pred3("a2", "c2", "d2"),
                pred3("b2", "d1", "c1"),
            }
        )

    def test_get_all_possible_transitions_multiple_independent_effects(self) -> None:
        domain_file = str(pddl_dir / "test_probabilistic_domain_alt.pddl")
        problem_dir = str(pddl_dir / "test_probabilistic_domain_alt")

        env = PDDLEnv(
            domain_file,
            problem_dir,
            raise_error_on_invalid_action=True,
            dynamic_action_space=True,
        )

        obs, _ = env.reset()
        action = env.action_space.all_ground_literals(obs).pop()
        transitions = env.get_all_possible_transitions(action)

        transition_list = list(transitions)
        assert len(transition_list) == 4

        s0, _, _, _ = transition_list[0]
        s1, _, _, _ = transition_list[1]
        s2, _, _, _ = transition_list[2]
        s3, _, _, _ = transition_list[3]
        states = set({s0.literals, s1.literals, s2.literals, s3.literals})

        type1 = Type("type1")
        type2 = Type("type2")
        pred1 = Predicate("pred1", 1, [type1])
        pred2 = Predicate("pred2", 1, [type2])
        pred3 = Predicate("pred3", 3, [type1, type2, type2])

        expected_states = set(
            {
                frozenset(
                    {pred1("b2"), pred3("a1", "c1", "d1"), pred3("a2", "c2", "d2")}
                ),
                frozenset(
                    {
                        pred1("b2"),
                        pred3("a1", "c1", "d1"),
                        pred3("a2", "c2", "d2"),
                        pred3("b2", "d1", "c1"),
                    }
                ),
                frozenset(
                    {
                        pred1("b2"),
                        pred2("c1"),
                        pred3("a1", "c1", "d1"),
                        pred3("a2", "c2", "d2"),
                    }
                ),
                frozenset(
                    {
                        pred1("b2"),
                        pred2("c1"),
                        pred3("a1", "c1", "d1"),
                        pred3("a2", "c2", "d2"),
                        pred3("b2", "d1", "c1"),
                    }
                ),
            }
        )

        assert states == expected_states

        # Now test again with return_probs=True.
        transitions = env.get_all_possible_transitions(action, return_probs=True)

        transition_list = list(transitions)
        assert len(transition_list) == 4
        s0, _, _, _ = transition_list[0][0]
        s1, _, _, _ = transition_list[1][0]
        s2, _, _, _ = transition_list[2][0]
        s3, _, _, _ = transition_list[3][0]
        states_and_probs = {
            s0.literals: transition_list[0][1],
            s1.literals: transition_list[1][1],
            s2.literals: transition_list[2][1],
            s3.literals: transition_list[3][1],
        }

        type1 = Type("type1")
        type2 = Type("type2")
        pred1 = Predicate("pred1", 1, [type1])
        pred2 = Predicate("pred2", 1, [type2])
        pred3 = Predicate("pred3", 3, [type1, type2, type2])

        expected_states = {
            frozenset(
                {pred1("b2"), pred3("a1", "c1", "d1"), pred3("a2", "c2", "d2")}
            ): 0.225,
            frozenset(
                {
                    pred1("b2"),
                    pred3("a1", "c1", "d1"),
                    pred3("a2", "c2", "d2"),
                    pred3("b2", "d1", "c1"),
                }
            ): 0.075,
            frozenset(
                {
                    pred1("b2"),
                    pred2("c1"),
                    pred3("a1", "c1", "d1"),
                    pred3("a2", "c2", "d2"),
                }
            ): 0.525,
            frozenset(
                {
                    pred1("b2"),
                    pred2("c1"),
                    pred3("a1", "c1", "d1"),
                    pred3("a2", "c2", "d2"),
                    pred3("b2", "d1", "c1"),
                }
            ): 0.175,
        }

        for s, prob in states_and_probs.items():
            assert s in expected_states
            assert prob - expected_states[s] < 1e-5

    def test_get_all_possible_transitions_multiple_effects(self) -> None:
        domain_file = str(pddl_dir / "test_probabilistic_domain_alt_2.pddl")
        problem_dir = str(pddl_dir / "test_probabilistic_domain_alt_2")

        env = PDDLEnv(
            domain_file,
            problem_dir,
            raise_error_on_invalid_action=True,
            dynamic_action_space=True,
        )

        obs, _ = env.reset()
        action = env.action_space.all_ground_literals(obs).pop()
        transitions = env.get_all_possible_transitions(action)

        transition_list = list(transitions)
        assert len(transition_list) == 3

        s0, _, _, _ = transition_list[0]
        s1, _, _, _ = transition_list[1]
        s2, _, _, _ = transition_list[2]
        states = set({s0.literals, s1.literals, s2.literals})

        type1 = Type("type1")
        type2 = Type("type2")
        pred1 = Predicate("pred1", 1, [type1])
        pred2 = Predicate("pred2", 1, [type2])
        pred3 = Predicate("pred3", 3, [type1, type2, type2])

        expected_states = set(
            {
                frozenset(
                    {pred1("b2"), pred3("a1", "c1", "d1"), pred3("a2", "c2", "d2")}
                ),
                frozenset(
                    {pred2("c1"), pred3("a1", "c1", "d1"), pred3("a2", "c2", "d2")}
                ),
                frozenset(
                    {
                        pred1("b2"),
                        pred2("c1"),
                        pred3("a1", "c1", "d1"),
                        pred3("a2", "c2", "d2"),
                        pred3("b2", "d1", "c1"),
                    }
                ),
            }
        )

        assert states == expected_states

        # Now test again with return_probs=True.
        transitions = env.get_all_possible_transitions(action, return_probs=True)

        transition_list = list(transitions)
        assert len(transition_list) == 3
        s0, _, _, _ = transition_list[0][0]
        s1, _, _, _ = transition_list[1][0]
        s2, _, _, _ = transition_list[2][0]
        states_and_probs = {
            s0.literals: transition_list[0][1],
            s1.literals: transition_list[1][1],
            s2.literals: transition_list[2][1],
        }

        type1 = Type("type1")
        type2 = Type("type2")
        pred1 = Predicate("pred1", 1, [type1])
        pred2 = Predicate("pred2", 1, [type2])
        pred3 = Predicate("pred3", 3, [type1, type2, type2])

        expected_states = {
            frozenset(
                {pred1("b2"), pred3("a1", "c1", "d1"), pred3("a2", "c2", "d2")}
            ): 0.5,
            frozenset(
                {pred2("c1"), pred3("a1", "c1", "d1"), pred3("a2", "c2", "d2")}
            ): 0.4,
            frozenset(
                {
                    pred1("b2"),
                    pred2("c1"),
                    pred3("a1", "c1", "d1"),
                    pred3("a2", "c2", "d2"),
                    pred3("b2", "d1", "c1"),
                }
            ): 0.1,
        }

        for s, prob in states_and_probs.items():
            assert s in expected_states
            assert prob - expected_states[s] < 1e-5

    def test_get_all_possible_transitions_common_effects(self) -> None:
        domain_file = str(pddl_dir / "test_probabilistic_domain_alt_3.pddl")
        problem_dir = str(pddl_dir / "test_probabilistic_domain_alt_3")

        env = PDDLEnv(
            domain_file,
            problem_dir,
            raise_error_on_invalid_action=True,
            dynamic_action_space=True,
        )

        obs, _ = env.reset()
        all_actions = sorted(env.action_space.all_ground_literals(obs))
        assert len(all_actions) == 2

        for action in [
            # TODO: Uncommenting all_actions[0] will break this test due
            # to logic errors in _apply_effects()!
            # all_actions[0],
            all_actions[1],
        ]:
            transitions_list = list(env.get_all_possible_transitions(action))
            assert len(transitions_list) == 2

            s0, _, _, _ = transitions_list[0]
            s1, _, _, _ = transitions_list[1]
            states = set({s0.literals, s1.literals})

            pred_b = Predicate("b", 0, [])
            pred_c = Predicate("c", 0, [])

            expected_states = set(
                {
                    frozenset({pred_b()}),
                    frozenset({pred_c()}),
                }
            )

            assert states == expected_states

        # Now test again with return_probs=True.
        for action in [
            # TODO: Uncommenting all_actions[0] will break this test due
            # to logic errors in _apply_effects()!
            # all_actions[0],
            all_actions[1],
        ]:
            transitions = list(
                env.get_all_possible_transitions(action, return_probs=True)
            )
            assert len(transitions) == 2
            s0, _, _, _ = transitions[0][0]
            s1, _, _, _ = transitions[1][0]
            states_and_probs = {
                s0.literals: transitions[0][1],
                s1.literals: transitions[1][1],
            }

            pred_b = Predicate("b", 0, [])
            pred_c = Predicate("c", 0, [])

            expected_states = {
                frozenset({pred_b()}): 0.8,
                frozenset({pred_c()}): 0.2,
            }

            for s, prob in states_and_probs.items():
                assert s in expected_states
                assert prob - expected_states[s] < 1e-5

    def test_determinize(self) -> None:
        domain_file = str(pddl_dir / "test_probabilistic_domain.pddl")
        problem_dir = str(pddl_dir / "test_probabilistic_domain")

        env = PDDLEnv(
            domain_file,
            problem_dir,
            raise_error_on_invalid_action=True,
            dynamic_action_space=True,
        )
        env.domain.determinize()

        obs, _ = env.reset()
        action = env.action_space.all_ground_literals(obs).pop()
        transitions = env.get_all_possible_transitions(action, return_probs=True)

        transition_list = list(transitions)
        assert len(transition_list) == 1
        assert transition_list[0][1] == 1.0
        newstate, _, _, _ = transition_list[0][0]

        type1 = Type("type1")
        type2 = Type("type2")
        pred1 = Predicate("pred1", 1, [type1])
        pred2 = Predicate("pred2", 1, [type2])
        pred3 = Predicate("pred3", 3, [type1, type2, type2])

        assert newstate.literals == frozenset(
            {
                pred1("b2"),
                pred2("c1"),
                pred3("a1", "c1", "d1"),
                pred3("a2", "c2", "d2"),
                pred3("b2", "d1", "c1"),
            }
        )

    def test_conditional_effects(self) -> None:
        # Domain exercises:
        #   * `when` (conditional effect) on a single operator-parameter
        #     variable, exercised both when the condition holds and when it
        #     does not;
        #   * `forall (...) (when (...) ...)` (universal conditional effect)
        #     for both single- and multi-variable forall bindings.
        domain_file = str(pddl_dir / "test_conditional_domain.pddl")
        problem_dir = str(pddl_dir / "test_conditional_domain")

        env = PDDLEnv(
            domain_file,
            problem_dir,
            raise_error_on_invalid_action=True,
        )
        obs, _ = env.reset()

        block = Type("block")
        is_blue = Predicate("is-blue", 1, [block])
        is_red = Predicate("is-red", 1, [block])
        is_marked = Predicate("is-marked", 1, [block])
        flag = Predicate("flag", 0, [])
        act_cond = Predicate("act-conditional", 1, [block])
        act_universal = Predicate("act-universal", 0, [])
        b1, b2, b3 = block("b1"), block("b2"), block("b3")

        # init: (is-blue b1) (is-red b2) (is-blue b3) (flag).  The
        # action-predicate literals are filtered out of the observation, so
        # obs.literals contains only the four state fluents above.
        assert obs.literals == frozenset(
            {is_blue(b1), is_red(b2), is_blue(b3), flag()}
        ), obs.literals

        # Conditional effect: when (is-blue ?x) -> flip blue -> red.
        # Take act_cond on b2 (red, not blue). The `when` condition is False,
        # so `is-marked b2` is added (unconditional part), but no red/blue
        # flip happens.
        obs, _, _, _, _ = env.step(act_cond(b2))
        assert obs.literals == frozenset(
            {is_blue(b1), is_red(b2), is_blue(b3), flag(), is_marked(b2)}
        ), obs.literals

        # Conditional effect on b1 (blue). The `when` condition holds, so
        # b1 is flipped to red. `is-marked b1` is also added.
        obs, _, _, _, _ = env.step(act_cond(b1))
        assert obs.literals == frozenset(
            {
                is_red(b1),
                is_red(b2),
                is_blue(b3),
                flag(),
                is_marked(b1),
                is_marked(b2),
            }
        ), obs.literals

        # Universal conditional effect: forall (?b - block) when (is-blue ?b)
        # (flip).  `flag` is also removed by the unconditional tail of the effect.
        env.reset()
        obs, _, _, _, _ = env.step(act_universal())
        assert obs.literals == frozenset(
            {
                is_red(b1),
                is_red(b2),
                is_red(b3),
            }
        ), obs.literals

    def test_conditional_effects_multi_var_forall(self) -> None:
        # Exercises the multi-variable forall binding at runtime:
        #   (forall (?b1 - block ?b2 - block) (when (is-blue ?b1) (flip b1)))
        domain_file = str(pddl_dir / "test_conditional_domain.pddl")
        problem_dir = str(pddl_dir / "test_conditional_domain")

        env = PDDLEnv(
            domain_file,
            problem_dir,
            raise_error_on_invalid_action=True,
        )
        obs, _ = env.reset()

        block = Type("block")
        is_blue = Predicate("is-blue", 1, [block])
        is_red = Predicate("is-red", 1, [block])
        act_multi = Predicate("act-multi-var", 0, [])
        b1, b2, b3 = block("b1"), block("b2"), block("b3")
        flag = Predicate("flag", 0, [])

        assert obs.literals == frozenset(
            {is_blue(b1), is_red(b2), is_blue(b3), flag()}
        ), obs.literals

        # Initial state: b1 & b3 blue, b2 red, flag set.
        # The multi_var action converts all blue blocks to red (the second
        # forall variable is unused in the body, so it only multiplies the
        # iteration count), and removes flag.
        obs, _, _, _, _ = env.step(act_multi())
        assert is_red(b1) in obs.literals, "b1 should be red after multi_var"
        assert is_blue(b1) not in obs.literals, "b1 should not be blue"
        assert is_red(b3) in obs.literals, "b3 should be red"
        assert is_blue(b3) not in obs.literals, "b3 should not be blue"
        # b2 started red and stays red
        assert is_red(b2) in obs.literals
        # flag is getting unset
        assert flag() not in obs.literals


if __name__ == "__main__":
    unittest.main()
