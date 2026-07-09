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

# Maps plan file names to their problem index.
# Problem files are sorted alphabetically, so e.g. problem9.pddl
# is at a different index than 9. This mapping accounts for that.
domain_to_problem_idx = {
    "baking": 19,  # problem9.pddl is the 20th file alphabetically
    "blocks": 39,
    "briefcaseworld": 29,
    "driverlog": 19,
    "elevator": 19,
    "ferry": 19,
    "gripper": 4,
    "hanoi": 19,
    "minecraft": 29,
    "needle_sorting": 19,
    "needle_transfer": 19,
    "newspapers": 39,
    "open_stacks": 29,
    "rearrangement": 19,
    "ring_and_peg": 29,
    "rovers": 39,
    "satellite": 35,
    "schedule": 49,
    "search_and_rescue": 19,
    "spannerlearning": 9,
    "tpp": 29,
    "zenotravel": 19,
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
        if not correct_plans_dir.exists():
            return
        for plan_file in correct_plans_dir.iterdir():
            if not plan_file.is_file():
                continue
            env_name = domain_to_env[plan_file.name]
            prob = Problem(
                domain_prompt_file="",
                problem_prompt_file="",
                action_schema_prompt_file="",
                object_names_prompt_file="",
                domain_name=env_name,
                problem_idx=domain_to_problem_idx.get(plan_file.name, 9),
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
                problem_idx=domain_to_problem_idx.get(plan_file.name, 9),
            )
            assert not prob.goal_reached(plan_file), (
                f"Plan {plan_file} unexpectedly reached goal"
            )
