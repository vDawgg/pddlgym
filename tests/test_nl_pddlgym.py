from nl_pddlgym.nl_pddlgym import NlPddlGymDs, Problem

from tests.constants import pddl_dir


domain_to_env = {
    "baking": "PDDLEnvBaking",
    "blocks": "PDDLEnvBlocks_medium",
    "briefcaseworld": "PDDLEnvBriefcaseworld",
    "driverlog": "PDDLEnvDriverlog",
    "elevator": "PDDLEnvElevator",
    "ferry": "PDDLEnvFerry",
    "gripper": "PDDLEnvGripper",
    "hanoi": "PDDLEnvHanoi",
    "minecraft": "PDDLEnvMinecraft",
    "movie": "PDDLEnvMovie",
    "needle_sorting": "PDDLEnvNeedle_sorting",
    "needle_transfer": "PDDLEnvNeedle_transfer",
    "newspapers": "PDDLEnvNewspapers",
    "open_stacks": "PDDLEnvOpen_stacks",
    "rearrangement": "PDDLEnvRearrangement",
    "ring_and_peg": "PDDLEnvRing_and_peg",
    "rovers": "PDDLEnvRovers",
    "satellite": "PDDLEnvSatellite",
    "schedule": "PDDLEnvSchedule",
    "search_and_rescue": "PDDLSearchAndRescueLevel1",
    "spannerlearning": "PDDLEnvSpannerlearning",
    "tpp": "PDDLEnvTpp",
    "zenotravel": "PDDLEnvZenotravel",
}


class TestNlPddlGym:
    def test_split(self):
        ds = NlPddlGymDs()
        assert len(ds.train) == 488
        assert len(ds.val) == 123
        assert len(ds.test) == 100

    def test_shuffle(self):
        ds_1 = NlPddlGymDs(shuffle_ds=False)
        ds_2 = NlPddlGymDs(shuffle_ds=False)
        assert not all(
            x.problem_prompt_file == y.problem_prompt_file
            for x, y in zip(ds_1.train, ds_2.train)
        )
        ds_1 = NlPddlGymDs(shuffle_ds=True)
        ds_2 = NlPddlGymDs(shuffle_ds=True)
        assert all(
            x.problem_prompt_file == y.problem_prompt_file
            for x, y in zip(ds_1.train, ds_2.train)
        )
        ds_1 = NlPddlGymDs(shuffle_ds=42)
        ds_2 = NlPddlGymDs(shuffle_ds=42)
        assert all(
            x.problem_prompt_file == y.problem_prompt_file
            for x, y in zip(ds_1.train, ds_2.train)
        )

    def test_all_envs_load(self):
        ds = NlPddlGymDs()
        for prob in ds.train + ds.val + ds.test:
            print(prob.domain_prompt_file)
            prob.goal_reached(pddl_dir / "mock_plan.pddl")

    def test_dspy_ds(self):
        ds = NlPddlGymDs()
        ds.make_dspy_ds()

    def test_correct_plans_goal_reached(self):
        correct_plans_dir = pddl_dir / "correct_plans"
        for plan_file in correct_plans_dir.iterdir():
            env_name = domain_to_env[plan_file.name]
            prob = Problem(
                domain_prompt_file="",
                problem_prompt_file="",
                action_schema_prompt_file="",
                object_names_prompt_file="",
                domain_name=env_name,
                problem_idx=9,
            )
            assert prob.goal_reached(plan_file), f"Plan {plan_file} does not reach goal"

    def test_incorrect_plans_goal_not_reached(self):
        incorrect_plans_dir = pddl_dir / "incorrect_plans"
        if not incorrect_plans_dir.exists():
            return
        for plan_file in incorrect_plans_dir.iterdir():
            if not plan_file.is_file():
                continue
            env_name = domain_to_env[plan_file.name]
            prob = Problem(
                domain_prompt_file="",
                problem_prompt_file="",
                action_schema_prompt_file="",
                object_names_prompt_file="",
                domain_name=env_name,
                problem_idx=9,
            )
            assert not prob.goal_reached(plan_file), (
                f"Plan {plan_file} unexpectedly reached goal"
            )
