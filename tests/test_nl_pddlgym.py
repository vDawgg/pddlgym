from pddlgym.nl_pddlgym import NlPddlGymDs, Problem

from tests.constants import pddl_dir


class TestNlPddlGym:
    def test_split(self):
        ds = NlPddlGymDs(split=(80, 20))
        print(ds.train, ds.val, ds.test)
        assert len(ds.train) == 283
        assert len(ds.val) == 0
        assert len(ds.test) == 73
        ds = NlPddlGymDs(split=(70, 15, 15))
        print(ds.train, ds.val, ds.test)
        assert len(ds.train) == 247
        assert len(ds.val) == 59
        assert len(ds.test) == 50

    def test_shuffle(self):
        ds_1 = NlPddlGymDs(shuffle_ds=False)
        ds_2 = NlPddlGymDs(shuffle_ds=False)
        assert all(
            x.problem_prompt_file == y.problem_prompt_file
            for x, y in zip(ds_1.train, ds_2.train)
        )
        ds_1 = NlPddlGymDs(shuffle_ds=True)
        ds_2 = NlPddlGymDs(shuffle_ds=True)
        assert not all(
            x.problem_prompt_file == y.problem_prompt_file
            for x, y in zip(ds_1.train, ds_2.train)
        )

    def test_all_envs_load(self):
        ds = NlPddlGymDs()
        for prob in ds.train + ds.val + ds.test:
            prob.goal_reached(pddl_dir / "mock_plan.pddl")

    def test_dspy_ds(self):
        ds = NlPddlGymDs()
        ds.make_dspy_ds()

    def test_goal_reached(self):
        prob = Problem(
            domain_prompt_file="Blocks.md",
            problem_prompt_file="Blocks_0.md",
            action_schema_prompt_file="Blocks.md",
            object_names_prompt_file="Blocks.md",
            domain_name="PDDLEnvBlocks",
            problem_idx=0,
        )
        assert prob.goal_reached(pddl_dir / "mock_plan_goal_reached.pddl")

    def test_goal_not_reached(self):
        prob = Problem(
            domain_prompt_file="Blocks.md",
            problem_prompt_file="Blocks_0.md",
            action_schema_prompt_file="Blocks.md",
            object_names_prompt_file="Blocks.md",
            domain_name="PDDLEnvBlocks",
            problem_idx=0,
        )
        assert not prob.goal_reached(pddl_dir / "mock_plan_goal_not_reached.pddl")
