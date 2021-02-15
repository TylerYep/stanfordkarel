# flake8: noqa
# pylint: disable=line-too-long
from conftest import PROBLEMS
from stanfordkarel.karel import KarelProgram
from stanfordkarel.karel_ascii import karel_ascii


def test_karel_ascii() -> None:
    karel = KarelProgram(PROBLEMS[4])
    result = karel_ascii(karel.world, *karel.world.karel_starting_location)

    assert result == (  # noqa
        "┌───────────────────────────────────────────────────────────────────────────────┐\n"
        "│   ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·   │\n"
        "│                                                                               │\n"
        "│   ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·   │\n"
        "│                                                                               │\n"
        "│   ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·   │\n"
        "│                                                                               │\n"
        "│   ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·   │\n"
        "│                                                                               │\n"
        "│   ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·   │\n"
        "│                                                                               │\n"
        "│   ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·   │\n"
        "│            ┌─────┐                 ┌─────┐                 ┌─────┐            │\n"
        "│   ·     ·  │  ·  │  ·     ·     ·  │  ·  │  ·     ·     ·  │  ·  │  ·     ·   │\n"
        "│      ┌─────┘     └─────┐     ┌─────┘     └─────┐     ┌─────┘     └─────┐      │\n"
        "│   ·  │  ·     ·     ·  │  ·  │  ·     ·     ·  │  ·  │  ·     ·     ·  │  ·   │\n"
        "│ ─────┘                 └─────┘                 └─────┘                 └───── │\n"
        "│  <1>    ·     ·     ·     ·     ·     ·     ·    <1>    ·     ·     ·    <1>  │\n"
        "│                                                                               │\n"
        "│  <1>    ·     ·     ·    <1>    ·     ·     ·     ·     ·     ·     ·     ·   │\n"
        "│                                                                               │\n"
        "│   ·     ·     ·     ·     ·     ·     ·     ·    <1>    ·     ·     ·    <1>  │\n"
        "│                                                                               │\n"
        "│   ·     ·     ·     ·    <1>    ·     ·     ·     ·     ·     ·     ·     ·   │\n"
        "│                                                                               │\n"
        "│   K     ·     ·     ·    <1>    ·     ·     ·     ·     ·     ·     ·    <1>  │\n"
        "└───────────────────────────────────────────────────────────────────────────────┘\n"
    )
