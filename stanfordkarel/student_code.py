"""
This file defines the StudentCode class, which is responsible for
loading and running a student's Karel program.

Original Author: Nicholas Bowman
Credits: Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
"""

from __future__ import annotations

import importlib.util
import inspect
from types import ModuleType
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


class StudentModule(ModuleType):
    move: Any
    turn_left: Any
    put_beeper: Any
    pick_beeper: Any
    paint_corner: Any

    @staticmethod
    def main() -> None:
        raise NotImplementedError


class StudentCode:
    """
    This process extracts a module from an arbitary file that contains student code.
    https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    """

    def __init__(
        self, code_file: Path | None = None, main_func: Callable[[], None] | None = None
    ) -> None:
        if main_func is not None:
            # Allow for passing in a main function directly for testing purposes
            self.mod = inspect.getmodule(main_func)
            if self.mod is not None:
                self.module_name = self.mod.__name__
            else:
                self.module_name = "student_module"
            return

        if code_file is None or not code_file.is_file():
            raise FileNotFoundError(f"{code_file} could not be found.")

        self.module_name = code_file.stem
        spec = importlib.util.spec_from_file_location(
            self.module_name, code_file.resolve()
        )
        assert spec is not None
        module_loader = spec.loader
        assert module_loader is not None
        mod = cast("StudentModule", importlib.util.module_from_spec(spec))
        self.mod = mod
        module_loader.exec_module(mod)

        if not hasattr(self.mod, "main"):
            raise RuntimeError(
                "Couldn't find the main() function. Are you sure you have one?"
            )

    def __repr__(self) -> str:
        if self.mod is None:
            return "<StudentCode: Module not loaded>"
        return inspect.getsource(self.mod)

    def main(self) -> None:
        if self.mod is None:
            raise RuntimeError("Module not loaded.")
        self.mod.main()
