"""
This file contains all of the constant and class definitions used
throughout the Karel library. Constants here define drawing proportions
for Karel and its world, initial world parameters, and different exception
and enumeration types, among other things.

Original Author: Nicholas Bowman
Credits: Kylie Jue, Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
Last Modified: 3/31/2020
"""
from enum import Enum, unique


@unique
class Direction(Enum):
    EAST = "east"
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"

    def __repr__(self) -> str:
        return str(self.value)


# Karel Application + World Editor
PAD_X = 75
PAD_Y = 10
LIGHT_GREY = "#e5e5e5"

# Karel Application + World Editor + Karel Canvas
DEFAULT_ICON = "karel"

# Karel, World Editor, Karel World
INFINITY = -1
COLOR_MAP = {
    "Red": "red",
    "Black": "black",
    "Cyan": "cyan",
    "Dark Gray": "gray30",
    "Gray": "gray55",
    "Green": "green",
    "Light Gray": "gray80",
    "Magenta": "magenta3",
    "Orange": "orange",
    "Pink": "pink",
    "White": "snow",
    "Blue": "blue",
    "Yellow": "yellow",
}


# Karel World, Karel Canvas
class Wall:
    """ Note that the World Editor only uses West & South to denote wall directions. """

    def __init__(self, avenue, street, direction):
        self.avenue = avenue
        self.street = street
        self.direction = direction

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash((self.avenue, self.street, self.direction))

    def __repr__(self):
        return f"Wall({self.avenue}, {self.street}, {self.direction})"


# Karel Application + Karel
class KarelException(Exception):
    """ The following classes define Karel-specific exceptions. """

    def __init__(self, avenue, street, direction, message):
        super().__init__()
        self.avenue = avenue
        self.street = street
        self.direction = direction.value.capitalize()
        self.message = message

    def __str__(self):
        return (
            f"Karel crashed while on avenue {self.avenue} and street {self.street}, "
            f"facing {self.direction}\nInvalid action: {self.message}"
        )
