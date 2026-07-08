"""Demonstrates basic PDDLGym usage with random action sampling"""

from __future__ import annotations

import matplotlib

matplotlib.use("agg")  # For rendering

from typing import cast
from nl_pddlgym.utils import run_demo
from nl_pddlgym.core import PDDLEnv
import nl_pddlgym


def demo_random(env_name, render=True, problem_index=0, verbose=True):
    env = cast(PDDLEnv, nl_pddlgym.make("PDDLEnv{}-v0".format(env_name.capitalize())))
    env.fix_problem_index(problem_index)

    def policy(s):
        return env.action_space.sample(s)

    video_path = "/tmp/{}_random_demo.mp4".format(env_name)
    run_demo(env, policy, render=render, verbose=verbose, seed=0, video_path=video_path)


def run_all(render=True, verbose=True):
    ## Some deterministic environments
    demo_random("gripper", render=render, verbose=verbose)
    demo_random("rearrangement", render=render, problem_index=6, verbose=verbose)
    demo_random("minecraft", render=render, verbose=verbose)
    demo_random("blocks", render=render, verbose=verbose)
    # demo_random("quantifiedblocks", render=render, verbose=verbose)
    # demo_random("fridge", render=render, verbose=verbose)


if __name__ == "__main__":
    run_all(render=False, verbose=True)
