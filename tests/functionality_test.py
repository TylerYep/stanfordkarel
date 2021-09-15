import pytest

from conftest import PROBLEMS, STUDENT_CODE_DIR, TIMEOUT, execute_karel_code


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.parametrize("problem_name", PROBLEMS)
def test_student_functionality(problem_name: str) -> None:
    code_file = STUDENT_CODE_DIR / f"{problem_name}.py"
    execute_karel_code(code_file)
