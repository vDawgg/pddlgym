from .minecraft import render as minecraft_render
from .rearrangement import render as rearrangement_render
from .sokoban import render as sokoban_render
from .hanoi import render as hanoi_render
from .blocks import render as blocks_render
from .explodingblocks import render as exploding_blocks_render
from .doors import render as doors_render
from .tsp import render as tsp_render
from .slidetile import render as slidetile_render
from .tireworld import render as tireworld_render
from .snake import render as snake_render
from .searchandrescue import render as sar_render  # noqa: F401
from .slow_searchandrescue import render as slow_sar_render  # noqa: F401
from .posar import render as posar_render  # noqa: F401
from .myopic_posar import render as myopic_posar_render  # noqa: F401
from .sar_render_from_string_grid import sar_render_from_string_grid  # noqa: F401
from .hiking import render as hiking_render
from .maze import render as maze_render
from .navigation import render as navigation_render
from .visit_all import render as visit_all_render

__all__ = [
    "minecraft_render",
    "rearrangement_render",
    "sokoban_render",
    "hanoi_render",
    "blocks_render",
    "exploding_blocks_render",
    "doors_render",
    "tsp_render",
    "slidetile_render",
    "tireworld_render",
    "snake_render",
    "sar_render",
    "slow_sar_render",
    "posar_render",
    "myopic_posar_render",
    "sar_render_from_string_grid",
    "hiking_render",
    "maze_render",
    "navigation_render",
    "visit_all_render",
]
