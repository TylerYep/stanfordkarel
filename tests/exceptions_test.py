import sys
from pathlib import Path

import pytest

from tests.conftest import execute_karel_code

IGNORED_FILES = {"__init__.py"}
TEST_CASES = (
    ("name_error.txt", "name 'turn_let' is not defined. Did you mean 'turn_left'?"),
    (
        "syntax_error.txt",
        (
            "invalid syntax (syntax_error.py, line 9)"
            if sys.version_info < (3, 10)
            else "'(' was never closed (syntax_error.py, line 5)"
        ),
    ),
    ("indent_error.txt", "unexpected indent (indent_error.py, line 7)"),
    (
        "missing_main.txt",
        "Couldn't find the main() function. Are you sure you have one?",
    ),
)


@pytest.mark.parametrize(("code_file", "expected_error"), TEST_CASES)
def test_exceptions(tmp_path: Path, code_file: str, expected_error: str) -> None:
    txt_file_contents = Path(f"tests/programs/{code_file}").read_text(encoding="utf-8")
    py_path = (tmp_path / code_file).with_suffix(".py")
    py_path.write_text(txt_file_contents)
    execute_karel_code(
        py_path, world_name="collect_newspaper_karel", expected_error=expected_error
    )


def test_file_coverage() -> None:
    """Test that all test cases are used."""
    tested_files = {filepath for filepath, _ in TEST_CASES}
    test_programs = {
        filepath.name
        for filepath in Path("tests/programs").glob("*.txt")
        if filepath.name not in IGNORED_FILES
    }
    untested_files = tested_files ^ test_programs
    assert not untested_files, untested_files
