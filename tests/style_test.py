import warnings

import pytest

from stanfordkarel.style_checker import StyleChecker
from tests.conftest import PROBLEMS, STUDENT_CODE_DIR, TIMEOUT


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.parametrize("problem_name", PROBLEMS)
def test_student_style(problem_name: str) -> None:
    code_file = STUDENT_CODE_DIR / f"{problem_name}.py"
    if code_file.is_file():
        StyleChecker(code_file).check_style()
    else:
        warnings.warn(
            "solutions/ code directory does not exist. Pass the tests for CI, "
            "but raise an error for actual student code.",
            stacklevel=2,
        )
