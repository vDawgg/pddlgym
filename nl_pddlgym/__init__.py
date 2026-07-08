"""Gym environment registration"""

from __future__ import annotations

from nl_pddlgym import core  # noqa: F401
from nl_pddlgym.core import PDDLEnv
from nl_pddlgym import structs  # noqa: F401
from nl_pddlgym import spaces  # noqa: F401

from nl_pddlgym.rendering import (
    rearrangement_render,
    minecraft_render,
    blocks_render,
    hanoi_render,
    navigation_render,
)
from gymnasium.envs.registration import register
import gymnasium as gym

import os
from typing import Callable, Dict, List, Tuple, Union, cast


# Save users from having to separately import gym
def make(*args, **kwargs) -> gym.Env:
    # env checker fails since obs is not an numpy array like object
    return gym.make(*args, disable_env_checker=True, **kwargs).unwrapped


def register_pddl_env(name: str, is_test_env: bool, other_args: dict) -> None:
    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pddl")
    domain_file = os.path.join(dir_path, "{}.pddl".format(name.lower()))
    gym_name = name.capitalize()
    problem_dirname = name.lower()
    if is_test_env:
        gym_name += "Test"
        problem_dirname += "_test"
    problem_dir = os.path.join(dir_path, problem_dirname)

    register(
        id="PDDLEnv{}-v0".format(gym_name),
        entry_point="nl_pddlgym.core:PDDLEnv",
        kwargs=dict(
            {"domain_file": domain_file, "problem_dir": problem_dir, **other_args}
        ),
    )


def _make_nav_render(name: str) -> Callable:
    return lambda obs: navigation_render(obs, cast(PDDLEnv, make(name)).domain)


_env_specs: List[Tuple[str, Dict[str, Union[bool, Callable]]]] = [
    ("gripper", {}),
    ("rearrangement", {"render": rearrangement_render}),
    ("minecraft", {"render": minecraft_render}),
    ("depot", {}),
    ("baking", {}),
    ("blocks", {"render": blocks_render}),
    ("hanoi", {"render": hanoi_render}),
    ("elevator", {}),
    ("ferry", {}),
    (
        "blocks_medium",
        {
            "render": blocks_render,
        },
    ),
    ("manygripper", {}),
    ("movie", {"operators_as_actions": True}),
    ("newspapers", {}),
    ("spannerlearning", {}),
    ("briefcaseworld", {}),
    ("driverlog", {}),
    ("needle_sorting", {}),
    ("needle_transfer", {}),
    ("open_stacks", {}),
    ("ring_and_peg", {}),
    ("rovers", {}),
    ("satellite", {}),
    ("schedule", {"operators_as_actions": True}),
    ("tpp", {}),
    ("zenotravel", {}),
]
for env_name, kwargs in _env_specs:
    other_args: Dict[str, Union[bool, Callable]] = {
        "raise_error_on_invalid_action": False,
    }
    kwargs.update(other_args)
    for is_test in [False, True]:
        register_pddl_env(env_name, is_test, kwargs)


# Custom environments
for level in range(1, 3):
    register(
        id=f"SearchAndRescueLevel{level}-v0",
        entry_point="nl_pddlgym.custom.searchandrescue:SearchAndRescueEnv",
        kwargs={"level": level, "test": False, "render_version": "slow"},
    )
    register(
        id=f"SearchAndRescueLevel{level}Test-v0",
        entry_point="nl_pddlgym.custom.searchandrescue:SearchAndRescueEnv",
        kwargs={"level": level, "test": True, "render_version": "slow"},
    )
    register(
        id=f"PDDLSearchAndRescueLevel{level}-v0",
        entry_point="nl_pddlgym.custom.searchandrescue:PDDLSearchAndRescueEnv",
        kwargs={"level": level, "test": False, "render_version": "slow"},
    )
    register(
        id=f"PDDLSearchAndRescueLevel{level}Test-v0",
        entry_point="nl_pddlgym.custom.searchandrescue:PDDLSearchAndRescueEnv",
        kwargs={"level": level, "test": True, "render_version": "slow"},
    )

register(
    id="SmallPOSARRadius1-v0",
    entry_point="nl_pddlgym.custom.searchandrescue:SmallPOSARRadius1Env",
)

register(
    id="SmallPOSARRadius0-v0",
    entry_point="nl_pddlgym.custom.searchandrescue:SmallPOSARRadius0Env",
)

register(
    id="POSARRadius1-v0",
    entry_point="nl_pddlgym.custom.searchandrescue:POSARRadius1Env",
)

register(
    id="POSARRadius1Xray-v0",
    entry_point="nl_pddlgym.custom.searchandrescue:POSARRadius1XrayEnv",
)

register(
    id="POSARRadius0-v0",
    entry_point="nl_pddlgym.custom.searchandrescue:POSARRadius0Env",
)

register(
    id="POSARRadius0Xray-v0",
    entry_point="nl_pddlgym.custom.searchandrescue:POSARRadius0XrayEnv",
)


register(
    id="SmallMyopicPOSAR-v0",
    entry_point="nl_pddlgym.custom.searchandrescue:SmallMyopicPOSAREnv",
)

register(
    id="TinyMyopicPOSAR-v0",
    entry_point="nl_pddlgym.custom.searchandrescue:TinyMyopicPOSAREnv",
)


# Ignore certain files for pdoc documentation generation.
__pdoc__ = {"downward_translate": False, "procedural_generation": False}
