"""Demonstrates PDDLGym usages with PDDLGym Planners

See https://github.com/ronuchit/pddlgym_planners
"""

from __future__ import annotations

import matplotlib

matplotlib.use("agg")  # For rendering

from nl_pddlgym.utils import run_demo
from nl_pddlgym.core import PDDLEnv
import nl_pddlgym
import copy

try:
    from pddlgym_planners.fd import FD  # type: ignore
    from pddlgym_planners.planner import PlanningFailure  # type: ignore
except ModuleNotFoundError:
    raise Exception(
        "To run this demo file, install the "
        + "PDDLGym Planners repository (https://github.com/ronuchit/pddlgym_planners)"
    )


def create_single_plan_policy(env, planner):
    plan = None

    def policy(s):
        nonlocal plan
        if plan is None:
            plan = planner(env.domain, s)
        assert plan is not None
        return plan.pop(0)

    return policy


def create_replanning_policy(env, planner):
    plan = None
    planning_failed = False
    domain = copy.deepcopy(env.domain)
    domain.determinize()

    def policy(s):
        nonlocal plan
        nonlocal planning_failed
        if not planning_failed:
            try:
                plan = planner(domain, s)
            except PlanningFailure:
                planning_failed = True
        if planning_failed:
            # Default to random actions
            return env.action_space.sample(s)
        assert plan is not None
        return plan.pop(0)

    return policy


def demo_planning(
    env_name, render=True, probabilistic=False, problem_index=0, verbose=True
):
    env = nl_pddlgym.make("PDDLEnv{}-v0".format(env_name.capitalize()))
    assert isinstance(env, PDDLEnv)
    env.fix_problem_index(problem_index)
    planner = FD(alias_flag="--alias lama-first")
    if probabilistic:
        policy = create_replanning_policy(env, planner)
    else:
        policy = create_single_plan_policy(env, planner)
    video_path = "/tmp/{}_planner_demo.mp4".format(env_name)
    run_demo(env, policy, render=render, verbose=verbose, seed=0, video_path=video_path)


def run_all(render=True, verbose=True):
    ## Some probabilistic environments
    demo_planning("explodingblocks", probabilistic=True, render=render, verbose=verbose)
    demo_planning("tireworld", probabilistic=True, render=render, verbose=verbose)
    demo_planning("river", probabilistic=True, render=render, verbose=verbose)

    ## Some deterministic environments
    demo_planning("sokoban", render=render, verbose=verbose)
    demo_planning("gripper", render=render, verbose=verbose)
    demo_planning("rearrangement", render=render, problem_index=6, verbose=verbose)
    demo_planning("minecraft", render=render, verbose=verbose)
    demo_planning("blocks", render=render, verbose=verbose)
    demo_planning("blocks_operator_actions", render=render, verbose=verbose)
    demo_planning("quantifiedblocks", render=render, verbose=verbose)
    demo_planning("fridge", render=render, verbose=verbose)


if __name__ == "__main__":
    run_all(render=False, verbose=True)
