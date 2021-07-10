"""
This file defines the Style Checker for Karel programs.

Original Author: Tyler Yep
Credits: Brahm Capoor
License: MIT
Version: 1.0.0
Email: tyep@cs.stanford.edu
"""
import ast
import inspect
from pathlib import Path
from typing import Any, Callable

import stanfordkarel

from .karel_application import StudentCode


def style_test(func: Callable[..., bool]) -> Callable[..., bool]:
    """Decorator for printing out the results of a style test."""

    def success_func(*args: Any, **kwargs: Any) -> bool:
        result = func(*args, **kwargs)
        if result:
            print("All good!")
        else:
            print("Error!")
        return result

    return success_func


class StyleChecker:
    """Style Checker for Karel."""

    def __init__(self, code_file: Path) -> None:
        self.student_code = StudentCode(code_file)
        self.modules = self.student_code.mods
        self.module_lines = str(self.student_code).split("\n")
        module_member_list = [inspect.getmembers(mod) for mod in self.modules]
        self.function_list = [
            var_name
            for var_name, value in
            # flatten module_member_list
            [m for module_members in module_member_list for m in module_members]
            if inspect.isfunction(value)
        ]

    @staticmethod
    def print_status_message(message: str) -> None:
        print(message.ljust(64), end="")

    def check_style(self) -> None:
        print(f"\n\nStyle Tests for {self.student_code.module_name}:")
        assert self.check_line_lengths()
        assert self.check_function_defs()
        assert self.assert_num_functions()
        assert self.check_recursion()
        assert self.check_naming()

    @style_test
    def check_recursion(self) -> bool:
        self.print_status_message("Checking for recursion...")
        return True

    @style_test
    def check_line_lengths(self, max_line_length: int = 88) -> bool:
        self.print_status_message("Checking line lengths...")
        long_idxs = [
            i for i, line in enumerate(self.module_lines) if len(line) > max_line_length
        ]
        if long_idxs:
            print(f"Lines {long_idxs} are longer than {max_line_length} characters.\n")
        return len(long_idxs) == 0

    @style_test
    def check_function_defs(self, min_name_length: int = 5) -> bool:
        self.print_status_message("Checking function definitions...")
        ok = True
        seen_already = set()
        for f in self.function_list:
            if f in seen_already:
                print(f"There are multiple functions defined that are called {f}")
                ok = False
            seen_already.add(f)
            if len(f) < min_name_length and f not in ("main", "move"):
                print(f"Function {f} has a pretty short name.")
                ok = False
        return ok

    @style_test
    def check_naming(self, min_name_length: int = 5) -> bool:
        """."""
        self.print_status_message("Checking function and variable names...")
        stanfordkarel_names = dir(stanfordkarel)
        root = ast.parse(str(self.student_code))
        names = sorted(
            {node.id for node in ast.walk(root) if isinstance(node, ast.Name)}
        )
        filtered_names = [name for name in names if name not in stanfordkarel_names]

        short_names = [
            f
            for f in filtered_names
            if len(f) < min_name_length and f not in ("main", "_")
        ]
        if short_names:
            print(f"Functions {short_names} have pretty short names.")
        return len(short_names) == 0

    @style_test
    def assert_num_functions(self, min_required: int = 10) -> bool:
        """
        Check that *at least* `num` functions
        are present in the module.
        """
        self.print_status_message("Checking number of functions...")
        num_fns = len(self.function_list)
        if num_fns < min_required:
            print(f"Expected at least {min_required} functions, only found {num_fns}.")
        return num_fns >= min_required
