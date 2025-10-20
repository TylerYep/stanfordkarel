"""
This file defines the shared logic for executing a student's Karel program,
handling namespace injection, action decoration, and error handling.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from .karel_program import KarelProgram
    from .student_code import StudentCode

import traceback

# List of all functions that should be injected into the student's namespace
KAREL_API_FUNCTIONS = [
    "move",
    "turn_left",
    "put_beeper",
    "pick_beeper",
    "paint_corner",
    "front_is_clear",
    "front_is_blocked",
    "left_is_clear",
    "left_is_blocked",
    "right_is_clear",
    "right_is_blocked",
    "beepers_present",
    "no_beepers_present",
    "beepers_in_bag",
    "no_beepers_in_bag",
    "facing_north",
    "not_facing_north",
    "facing_east",
    "not_facing_east",
    "facing_west",
    "not_facing_west",
    "facing_south",
    "not_facing_south",
    "corner_color_is",
]


def inject_karel_api(student_code: StudentCode, karel: KarelProgram) -> None:
    """
    Injects the Karel API functions from a KarelProgram object into a student's
    code module.
    """
    for func_name in KAREL_API_FUNCTIONS:
        setattr(student_code.mod, func_name, getattr(karel, func_name))


def execute_student_program(
    student_code: StudentCode,
    karel: KarelProgram,
    action_callback: Callable[[str], None] | None = None,
) -> bool:
    """
    Executes the student's main() function, handling API injection,
    action callbacks, and error handling.

    Returns True if the program executed without errors, False otherwise.
    """
    inject_karel_api(student_code, karel)

    if action_callback:
        karel.add_action_callback(action_callback)

    try:
        student_code.main()
    except Exception:  # noqa: BLE001
        print("\nAn error occurred during program execution:")
        traceback.print_exc()
        return False
    else:
        return True
