"""Utilities"""

from __future__ import annotations

from collections import defaultdict
import contextlib
import sys
import itertools
import gymnasium as gym
import imageio
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, cast


def get_object_combinations(
    objects: List,
    arity: int,
    var_types: Optional[List] = None,
    type_to_parent_types: Optional[Dict] = None,
    allow_duplicates: bool = False,
) -> Iterator[Tuple]:
    type_to_objs = defaultdict(list)

    for obj in sorted(objects):
        if type_to_parent_types is None:
            type_to_objs[obj.var_type].append(obj)
        else:
            for t in type_to_parent_types[obj.var_type]:
                type_to_objs[t].append(obj)

    if var_types is None:
        choices = [sorted(objects) for _ in range(arity)]
    else:
        assert len(var_types) == arity
        choices = [type_to_objs[vt] for vt in var_types]

    for choice in itertools.product(*choices):
        if not allow_duplicates and len(set(choice)) != len(choice):
            continue
        yield choice


def run_demo(
    env: gym.Env,
    policy: Callable,
    max_num_steps: int = 10,
    render: bool = False,
    video_path: Optional[str] = None,
    fps: int = 3,
    verbose: bool = False,
    seed: Optional[int] = None,
    check_reward: bool = False,
) -> None:

    images: List = []

    if seed is not None:
        cast(Any, env).seed(seed)

    obs, _ = env.reset()

    if seed is not None:
        env.action_space.seed(seed)

    tot_reward = 0.0

    for t in range(max_num_steps):
        if verbose:
            print("Obs:", obs)

        if render:
            images.append(env.render())

        action = policy(obs)
        if verbose:
            print("Act:", action)

        obs, reward, done, _, _ = env.step(action)
        env.render()
        tot_reward += float(reward)
        if verbose:
            print("Rew:", reward)

        if done:
            break

    if verbose:
        print("Final obs:", obs)
        print()

    if render:
        images.append(env.render())
        assert video_path is not None
        imageio.mimwrite(video_path, cast(List, images), fps=fps)
        print("Wrote out video to", video_path)

    env.close()
    if check_reward:
        assert tot_reward > 0
    if verbose:
        input("press enter to continue to next problem")


class DummyFile:
    def write(self, x: str) -> None:
        pass

    def flush(self) -> None:
        pass


@contextlib.contextmanager
def nostdout() -> Iterator[None]:
    save_stdout = sys.stdout
    sys.stdout = DummyFile()
    yield
    sys.stdout = save_stdout
