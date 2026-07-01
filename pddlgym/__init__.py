"""Gym environment registration"""

from __future__ import annotations

from . import tests  # noqa: F401
from . import core  # noqa: F401
from pddlgym.core import PDDLEnv
from . import structs  # noqa: F401
from . import spaces  # noqa: F401

from pddlgym.rendering import (
    rearrangement_render,
    sokoban_render,
    minecraft_render,
    blocks_render,
    doors_render,
    hanoi_render,
    tsp_render,
    slidetile_render,
    tireworld_render,
    snake_render,
    exploding_blocks_render,
    hiking_render,
    maze_render,
    navigation_render,
    visit_all_render,
)
from gym.envs.registration import register
import gym

import os
from typing import Callable, Dict, List, Tuple, Union, cast


# Save users from having to separately import gym
def make(*args, **kwargs) -> gym.Env:
    # env checker fails since obs is not an numpy array like object
    return gym.make(*args, disable_env_checker=True, **kwargs)


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
        entry_point="pddlgym.core:PDDLEnv",
        kwargs=dict(
            {"domain_file": domain_file, "problem_dir": problem_dir, **other_args}
        ),
    )


def _make_nav_render(name: str) -> Callable:
    return lambda obs: navigation_render(obs, cast(PDDLEnv, make(name)).domain)


_env_specs: List[Tuple[str, Dict[str, Union[bool, Callable]]]] = [
    ("gripper", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("easygripper", {"operators_as_actions": True, "dynamic_action_space": False}),
    ("onearmedgripper", {"operators_as_actions": True, "dynamic_action_space": False}),
    (
        "tinyonearmedgripper",
        {"operators_as_actions": True, "dynamic_action_space": False},
    ),
    (
        "lifelong_tiny_gripper",
        {"operators_as_actions": True, "dynamic_action_space": False},
    ),
    ("rearrangement", {"render": rearrangement_render}),
    ("sokoban", {"render": sokoban_render}),
    ("minecraft", {"render": minecraft_render}),
    ("depot", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("baking", {}),
    ("blocks", {"render": blocks_render}),
    ("derivedblocks", {"render": blocks_render}),
    ("toomanyblocks", {"render": blocks_render}),
    ("lifelong_blocks6", {"render": blocks_render}),
    ("travel", {}),
    ("doors", {"render": doors_render}),
    ("casino", {}),
    ("hanoi", {"render": hanoi_render}),
    (
        "hanoi_operator_actions",
        {
            "render": hanoi_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    ("tsp", {"render": tsp_render}),
    (
        "tsp_operator_actions",
        {
            "render": tsp_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    ("slidetile", {"render": slidetile_render}),
    ("elevator", {}),
    ("ferry", {}),
    ("meetpass", {}),
    ("footwear", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("easyblocks", {"render": blocks_render}),
    ("conditionalblocks", {"render": blocks_render}),
    ("conditionalferry", {}),
    (
        "blocks_operator_actions",
        {
            "render": blocks_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    (
        "generated_blocks",
        {
            "render": blocks_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    (
        "blocks_medium",
        {
            "render": blocks_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    (
        "manyblocksnopiles",
        {
            "render": blocks_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    (
        "manyexplodingblockssmallpiles",
        {
            "render": blocks_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    (
        "manyblockssmallpiles",
        {
            "render": blocks_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    (
        "manyblockssmallpilesnoclear",
        {
            "render": blocks_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    (
        "manyblockssmallpilesnohand",
        {
            "render": blocks_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    (
        "manyblockssmallpilesnoclearhand",
        {
            "render": blocks_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    (
        "quantifiedblocks",
        {
            "render": blocks_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    (
        "quantifiedblocks2",
        {
            "render": blocks_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    (
        "quantifiedblocks3",
        {
            "render": blocks_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    ("equalityblocks", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("equalityblocks2", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("manygrid", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("manylogistics", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("manymiconic", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("manygripper", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("manyferry", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("movie", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("glibblocks", {"render": blocks_render}),
    ("glibrearrangement", {"render": rearrangement_render}),
    ("glibdoors", {"render": doors_render}),
    ("tireworld", {"render": tireworld_render}),
    (
        "manytireworld",
        {
            "render": tireworld_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    ("fridge", {"operators_as_actions": True, "dynamic_action_space": True}),
    (
        "snake",
        {
            "render": snake_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
    ("river", {}),
    ("explodingblocks", {"render": exploding_blocks_render}),
    ("newspapers", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("easynewspapers", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("trapnewspapers", {"operators_as_actions": True, "dynamic_action_space": True}),
    (
        "hiking",
        {
            "operators_as_actions": True,
            "dynamic_action_space": True,
            "render": hiking_render,
        },
    ),
    (
        "maze",
        {
            "operators_as_actions": True,
            "dynamic_action_space": True,
            "render": maze_render,
        },
    ),
    ("spannerlearning", {"operators_as_actions": True, "dynamic_action_space": True}),
    ("navigation1", {"render": _make_nav_render("PDDLEnvNavigation1-v0")}),
    ("navigation2", {"render": _make_nav_render("PDDLEnvNavigation2-v0")}),
    ("navigation3", {"render": _make_nav_render("PDDLEnvNavigation3-v0")}),
    ("navigation4", {"render": _make_nav_render("PDDLEnvNavigation4-v0")}),
    ("navigation5", {"render": _make_nav_render("PDDLEnvNavigation5-v0")}),
    ("navigation6", {"render": _make_nav_render("PDDLEnvNavigation6-v0")}),
    ("navigation7", {"render": _make_nav_render("PDDLEnvNavigation7-v0")}),
    ("navigation8", {"render": _make_nav_render("PDDLEnvNavigation8-v0")}),
    ("navigation9", {"render": _make_nav_render("PDDLEnvNavigation9-v0")}),
    ("navigation10", {"render": _make_nav_render("PDDLEnvNavigation10-v0")}),
    (
        "visit_all",
        {
            "render": visit_all_render,
            "operators_as_actions": True,
            "dynamic_action_space": True,
        },
    ),
]
for env_name, kwargs in _env_specs:
    other_args: Dict[str, Union[bool, Callable]] = {
        "raise_error_on_invalid_action": False,
    }
    kwargs.update(other_args)
    for is_test in [False, True]:
        register_pddl_env(env_name, is_test, kwargs)


# Custom environments
for level in range(1, 8):
    register(
        id=f"SearchAndRescueLevel{level}-v0",
        entry_point="pddlgym.custom.searchandrescue:SearchAndRescueEnv",
        kwargs={"level": level, "test": False, "render_version": "slow"},
    )
    register(
        id=f"SearchAndRescueLevel{level}Test-v0",
        entry_point="pddlgym.custom.searchandrescue:SearchAndRescueEnv",
        kwargs={"level": level, "test": True, "render_version": "slow"},
    )
    register(
        id=f"PDDLSearchAndRescueLevel{level}-v0",
        entry_point="pddlgym.custom.searchandrescue:PDDLSearchAndRescueEnv",
        kwargs={"level": level, "test": False, "render_version": "slow"},
    )
    register(
        id=f"PDDLSearchAndRescueLevel{level}Test-v0",
        entry_point="pddlgym.custom.searchandrescue:PDDLSearchAndRescueEnv",
        kwargs={"level": level, "test": True, "render_version": "slow"},
    )

register(
    id="SmallPOSARRadius1-v0",
    entry_point="pddlgym.custom.searchandrescue:SmallPOSARRadius1Env",
)

register(
    id="SmallPOSARRadius0-v0",
    entry_point="pddlgym.custom.searchandrescue:SmallPOSARRadius0Env",
)

register(
    id="POSARRadius1-v0",
    entry_point="pddlgym.custom.searchandrescue:POSARRadius1Env",
)

register(
    id="POSARRadius1Xray-v0",
    entry_point="pddlgym.custom.searchandrescue:POSARRadius1XrayEnv",
)

register(
    id="POSARRadius0-v0",
    entry_point="pddlgym.custom.searchandrescue:POSARRadius0Env",
)

register(
    id="POSARRadius0Xray-v0",
    entry_point="pddlgym.custom.searchandrescue:POSARRadius0XrayEnv",
)


register(
    id="SmallMyopicPOSAR-v0",
    entry_point="pddlgym.custom.searchandrescue:SmallMyopicPOSAREnv",
)

register(
    id="TinyMyopicPOSAR-v0",
    entry_point="pddlgym.custom.searchandrescue:TinyMyopicPOSAREnv",
)


# Ignore certain files for pdoc documentation generation.
__pdoc__ = {"downward_translate": False, "procedural_generation": False}
