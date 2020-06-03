import pytest

from stanfordkarel.karel_world import KarelWorld


def test_checkerboard_karel():
    world = KarelWorld("checkerboard_karel")
    assert world


def test_checkerboard():
    with pytest.raises(FileNotFoundError):
        _ = KarelWorld("checkerboard")


def test_karl():
    with pytest.raises(FileNotFoundError):
        _ = KarelWorld("karl")
