import os

import pytest

from conftest import PROBLEMS, STUDENT_CODE_DIR, TIMEOUT
from stanfordkarel.style_checker import StyleChecker


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.parametrize("problem_name", PROBLEMS)
def test_karel_style(problem_name):
    code_file = os.path.join(STUDENT_CODE_DIR, problem_name + ".py")
    StyleChecker(code_file).check_style()
