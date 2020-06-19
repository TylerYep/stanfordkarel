import os

import pytest

from conftest import PROBLEMS, STUDENT_CODE_DIR, TIMEOUT, execute_karel_code


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.parametrize("problem_name", PROBLEMS)
def test_karel_functionality(problem_name):
    code_file = os.path.join(STUDENT_CODE_DIR, problem_name + ".py")
    execute_karel_code(code_file)
