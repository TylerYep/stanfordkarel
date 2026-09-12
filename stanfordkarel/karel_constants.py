"""
This file contains shared constants for the Karel renderers.

Author: Gemini Code Assist
"""

import math

from .karel_world import Direction

DIRECTION_TO_RADIANS = {
    Direction.EAST: 0,
    Direction.SOUTH: math.pi / 2,
    Direction.WEST: math.pi,
    Direction.NORTH: 3 * math.pi / 2,
}

# Karel Application + World Editor
DEFAULT_ICON = "karel"
PAD_X = 75
PAD_Y = 10
LIGHT_GREY = "#e5e5e5"

WALL_DETECTION_THRESHOLD = 0.1
BORDER_OFFSET = 17
LABEL_OFFSET = 7
CORNER_SIZE = 2
BEEPER_CELL_SIZE_FRAC = 0.4
LINE_WIDTH = 2
# Drawing Constants for Karel Robot Icon (defined relative to a single cell)
KAREL_VERTICAL_OFFSET = 0.05
KAREL_LEFT_HORIZONTAL_PAD = 0.29
KAREL_HEIGHT = 0.76
KAREL_WIDTH = 0.58
KAREL_INNER_HEIGHT = 0.38
KAREL_INNER_WIDTH = 0.28125
KAREL_INNER_OFFSET = 0.125
KAREL_MOUTH_WIDTH = 0.1375
KAREL_MOUTH_HORIZONTAL_OFFSET = 0.2625
KAREL_MOUTH_VERTICAL_OFFSET = 0.125
KAREL_UPPER_RIGHT_DIAG = 0.2
KAREL_LOWER_LEFT_DIAG = 0.13125
KAREL_LEG_LENGTH = 0.15
KAREL_FOOT_LENGTH = 0.1875
KAREL_LEG_FOOT_WIDTH = 0.075
KAREL_LEG_VERTICAL_OFFSET = 0.5
KAREL_LEG_HORIZONTAL_OFFSET = 0.2625
KAREL_LINE_WIDTH = 2
# Drawing Constants for Simple Karel Icon (defined relative to a single cell)
SIMPLE_KAREL_HEIGHT = 0.7
SIMPLE_KAREL_WIDTH = 0.8
