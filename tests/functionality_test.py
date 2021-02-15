import os
import warnings

import pytest

from conftest import PROBLEMS, STUDENT_CODE_DIR, TIMEOUT, execute_karel_code


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.parametrize("problem_name", PROBLEMS)
def test_student_functionality(problem_name: str) -> None:
    code_file = os.path.join(STUDENT_CODE_DIR, problem_name + ".py")
    if os.path.exists(code_file):
        execute_karel_code(code_file)
    else:
        warnings.warn(
            "Code directory does not exist. Pass the tests for travis-ci, "
            "but raise an error for actual student code."
        )
