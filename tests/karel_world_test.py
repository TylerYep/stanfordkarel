from pathlib import Path

from stanfordkarel.karel_application import StudentCode
from stanfordkarel.karel_program import KarelProgram

STONE_MASON_ASCII_OUTPUT = (
    "┌───────────────────────────────────────────────────────────────────────────────┐",
    "│   ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·   │",
    "│                                                                               │",
    "│   ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·   │",
    "│                                                                               │",
    "│   ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·   │",
    "│                                                                               │",
    "│   ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·   │",
    "│                                                                               │",
    "│   ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·   │",
    "│                                                                               │",
    "│   ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·     ·   │",
    "│            ┌─────┐                 ┌─────┐                 ┌─────┐            │",
    "│   ·     ·  │  ·  │  ·     ·     ·  │  ·  │  ·     ·     ·  │  ·  │  ·     ·   │",
    "│      ┌─────┘     └─────┐     ┌─────┘     └─────┐     ┌─────┘     └─────┐      │",
    "│   ·  │  ·     ·     ·  │  ·  │  ·     ·     ·  │  ·  │  ·     ·     ·  │  ·   │",
    "│ ─────┘                 └─────┘                 └─────┘                 └───── │",
    "│  <1>    ·     ·     ·     ·     ·     ·     ·    <1>    ·     ·     ·    <1>  │",
    "│                                                                               │",
    "│  <1>    ·     ·     ·    <1>    ·     ·     ·     ·     ·     ·     ·     ·   │",
    "│                                                                               │",
    "│   ·     ·     ·     ·     ·     ·     ·     ·    <1>    ·     ·     ·    <1>  │",
    "│                                                                               │",
    "│   ·     ·     ·     ·    <1>    ·     ·     ·     ·     ·     ·     ·     ·   │",
    "│                                                                               │",
    "│   K     ·     ·     ·    <1>    ·     ·     ·     ·     ·     ·     ·    <1>  │",
    "└───────────────────────────────────────────────────────────────────────────────┘",
)


class TestKarelWorld:
    @staticmethod
    def test_karel_ascii() -> None:
        karel = KarelProgram("stone_mason_karel")

        assert str(karel) == "\n".join(STONE_MASON_ASCII_OUTPUT) + "\n"

    @staticmethod
    def test_save_to_file(tmp_path: Path) -> None:
        karel = KarelProgram("stone_mason_karel")
        output_file = tmp_path / "test_world.w"
        karel.world.save_to_file(output_file)
        expected = (
            "Dimension: (13, 13)",
            "Wall: (1, 6); south",
            "Wall: (2, 6); west",
            "Wall: (2, 7); south",
            "Wall: (3, 7); west",
            "Wall: (3, 8); south",
            "Wall: (4, 7); south",
            "Wall: (4, 7); west",
            "Wall: (5, 6); south",
            "Wall: (5, 6); west",
            "Wall: (6, 6); west",
            "Wall: (6, 7); south",
            "Wall: (7, 7); west",
            "Wall: (7, 8); south",
            "Wall: (8, 7); south",
            "Wall: (8, 7); west",
            "Wall: (9, 6); south",
            "Wall: (9, 6); west",
            "Wall: (10, 6); west",
            "Wall: (10, 7); south",
            "Wall: (11, 7); west",
            "Wall: (11, 8); south",
            "Wall: (12, 7); south",
            "Wall: (12, 7); west",
            "Wall: (13, 6); south",
            "Wall: (13, 6); west",
            "Beeper: (1, 4); 1",
            "Beeper: (1, 5); 1",
            "Beeper: (5, 1); 1",
            "Beeper: (5, 2); 1",
            "Beeper: (5, 4); 1",
            "Beeper: (9, 3); 1",
            "Beeper: (9, 5); 1",
            "Beeper: (13, 1); 1",
            "Beeper: (13, 3); 1",
            "Beeper: (13, 5); 1",
            "Karel: (1, 1); east",
            "BeeperBag: INFINITY",
        )

        assert output_file.read_text() == "\n".join(expected) + "\n"

    @staticmethod
    def test_empty_beepers(tmp_path: Path) -> None:
        code_file = "empty_beeper.txt"
        txt_file_contents = Path(f"tests/programs/{code_file}").read_text(
            encoding="utf-8"
        )
        py_path = (tmp_path / code_file).with_suffix(".py")
        py_path.write_text(txt_file_contents)

        test_program = KarelProgram("1x1")

        test_code = StudentCode(py_path)
        test_code.inject_namespace(test_program)
        test_code.main()

        ref_program = KarelProgram("1x1")

        assert ref_program.world.get_beepers() == test_program.world.get_beepers()

    @staticmethod
    def test_empty_colors(tmp_path: Path) -> None:
        code_file = "empty_color.txt"
        txt_file_contents = Path(f"tests/programs/{code_file}").read_text(
            encoding="utf-8"
        )
        py_path = (tmp_path / code_file).with_suffix(".py")
        py_path.write_text(txt_file_contents)

        test_program = KarelProgram("1x1")

        test_code = StudentCode(py_path)
        test_code.inject_namespace(test_program)
        test_code.main()

        ref_program = KarelProgram("1x1")

        assert ref_program.world.get_beepers() == test_program.world.get_beepers()

    @staticmethod
    def test_equal_worlds() -> None:
        test_program = KarelProgram("1x1")
        ref_program = KarelProgram("1x1")

        assert ref_program.world == test_program.world
