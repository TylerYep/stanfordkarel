"""
This file defines the necessary functions and definitions that students must
import in order to be able to write a new Karel program. Any new Karel file
must include the following line:

from stanfordkarel import *

Original Author: Nicholas Bowman
Credits: Kylie Jue, Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
"""
import sys
import tkinter as tk
from pathlib import Path

from .karel_application import KarelApplication
from .karel_program import KarelProgram

# The following function definitions are defined as stubs so that IDEs can recognize
# the function definitions in student code. These names are re-bound upon program
# execution to asscoiate their behavior to the one particular Karel object located
# in a given world.


def move() -> None:
    pass


def turn_left() -> None:
    pass


def put_beeper() -> None:
    pass


def pick_beeper() -> None:
    pass


def front_is_clear() -> bool:
    pass


def front_is_blocked() -> bool:
    pass


def left_is_clear() -> bool:
    pass


def left_is_blocked() -> bool:
    pass


def right_is_clear() -> bool:
    pass


def right_is_blocked() -> bool:
    pass


def beepers_present() -> bool:
    pass


def no_beepers_present() -> bool:
    pass


def beepers_in_bag() -> bool:
    pass


def no_beepers_in_bag() -> bool:
    pass


def facing_north() -> bool:
    pass


def not_facing_north() -> bool:
    pass


def facing_east() -> bool:
    pass


def not_facing_east() -> bool:
    pass


def facing_west() -> bool:
    pass


def not_facing_west() -> bool:
    pass


def facing_south() -> bool:
    pass


def not_facing_south() -> bool:
    pass


def paint_corner(color: str) -> None:
    del color


def corner_color_is(color: str) -> bool:
    del color
    return True


# Defined constants for ease of use by students when coloring corners
RED = "Red"
BLACK = "Black"
CYAN = "Cyan"
DARK_GRAY = "Dark Gray"
GRAY = "Gray"
GREEN = "Green"
LIGHT_GRAY = "Light Gray"
MAGENTA = "Magenta"
ORANGE = "Orange"
PINK = "Pink"
WHITE = "White"
BLUE = "Blue"
YELLOW = "Yellow"
BLANK = ""


def run_karel_program(world_file: str = "") -> None:
    # Extract the name of the file the student is executing
    student_code_file = Path(sys.argv[0])

    # Special case - if filename matches a specified world name,
    # Set the default world to the world with that name.
    # I personally recommend removing this functionality completely.
    if (
        world_file == ""
        and (
            Path(__file__).absolute().parent
            / "worlds"
            / student_code_file.with_suffix(".w").name
        ).is_file()
    ):
        world_file = student_code_file.stem

    # Create Karel and assign it to live in the newly created world
    karel = KarelProgram(world_file)

    # Initialize root Tk Window and spawn Karel application
    root = tk.Tk()
    app = KarelApplication(karel, student_code_file, master=root)
    app.mainloop()
