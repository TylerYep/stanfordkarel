from pathlib import Path

import pytest

from conftest import TIMEOUT, execute_karel_code


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.parametrize("problem_name", ["error_1"])
def test_exceptions(problem_name: str) -> None:
    code_file = Path(f"tests/programs/{problem_name}.py")
    execute_karel_code(
        code_file,
        world_name="collect_newspaper_karel",
        expected_error="name 'turn_let' is not defined. Did you mean 'turn_left'?",
    )
