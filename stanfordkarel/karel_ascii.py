from enum import Enum, unique

from .karel_definitions import Direction

CHAR_WIDTH = 6
HORIZONTAL, VERTICAL = "─", "│"
SPACING = 10


class Tile:
    def __init__(self, value="·"):
        self.value = value
        self.walls = []
        self.beepers = 0
        self.color = ""

    def __repr__(self):
        result = ""
        if self.value == "K" and self.beepers > 0:
            result += " <K> "
        elif self.beepers > 0:
            result += f" <{self.beepers}> "
        elif self.color:
            result += f" {self.color[:3]} "
        else:
            result += f"  {self.value}  "
        return result


@unique
class Color(Enum):
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def compare_output(first, second):
    """ Compares Karel Output and gets the results. """

    def create_two_column_string(col1, col2):
        """ col1 and col2 are Lists. """
        return map(lambda x: f"{x[0]}{' ' * SPACING}{x[1]}", zip(col1, col2))

    def symmetric_difference(a, b):
        extra_a, extra_b = {}, {}
        for k in a:
            if k not in b:
                extra_a[k] = a[k]
            elif a[k] - b[k] > 0:
                extra_a[k] = a[k] - b[k]
        for k in b:
            if k not in a:
                extra_b[k] = b[k]
            elif b[k] - a[k] > 0:
                extra_b[k] = b[k] - a[k]
        return extra_a, extra_b

    # if not two_column_output:
    # print(f"\n\nStudent output:\n{self}")
    # print(f"\nExpected output:\n{other}")

    this, that = str(first).split("\n"), str(second).split("\n")
    world_width = len(this[0])

    header1, header2 = "Student Output:", "Expected Output:"
    text_spacing = " " * (world_width - len(header1) + SPACING + 1)
    two_columns = create_two_column_string(this, that)
    output = "\n".join(two_columns)
    fancy_arrows = f"{Color.RED.value}❯{Color.YELLOW.value}❯{Color.GREEN.value}❯ "

    result = (
        f"\n\n{fancy_arrows} {Color.YELLOW.value}{first.world.world_name}{Color.END.value}"
        f"\n{header1}{text_spacing}{header2}\n{output}\n"
    )

    if first.avenue != second.avenue or first.street != second.street:
        result += (
            f"Karel did not end up in the same location in both worlds:\n"
            f"Student: {(first.avenue, first.street)}\n"
            f"Expected: {(second.avenue, second.street)}\n\n"
        )
    if first.world.beepers != second.world.beepers:
        extra_a, extra_b = symmetric_difference(first.world.beepers, second.world.beepers)
        result += (
            f"Beepers do not match: "
            f"(Only beepers that appear in one world but not the other are listed)\n"
            f"Student: {extra_a}\n"
            f"Expected: {extra_b}\n\n"
        )
    return result


def karel_ascii(world, karel_street, karel_avenue):
    """ Creates a Karel World in ASCII Art! """

    def tile_pair_has_wall(r, c, direction):
        """ Checks if the tile at r, c should have a wall by checking itself and its neighbors. """

        def tile_has_wall(r, c, direction):
            if 0 <= r < world.num_streets and 0 <= c < world.num_avenues:
                tile = world_arr[r][c]
                return direction in tile.walls
            return False

        if direction == Direction.SOUTH:
            return tile_has_wall(r, c, Direction.SOUTH) or tile_has_wall(r + 1, c, Direction.NORTH)
        if direction == Direction.NORTH:
            return tile_has_wall(r, c, Direction.NORTH) or tile_has_wall(r - 1, c, Direction.SOUTH)
        if direction == Direction.WEST:
            return tile_has_wall(r, c, Direction.WEST) or tile_has_wall(r, c - 1, Direction.EAST)
        if direction == Direction.EAST:
            return tile_has_wall(r, c, Direction.EAST) or tile_has_wall(r, c + 1, Direction.WEST)

    def get_next_line(r, c, next_block_start):
        """ Given a tile, figures out what the lower line of the ASCII art should be. """

        if tile_pair_has_wall(r, c, Direction.SOUTH):
            if (
                next_block_start == HORIZONTAL
                and tile_pair_has_wall(r, c, Direction.WEST)
                and tile_pair_has_wall(r + 1, c, Direction.WEST)
            ):
                next_block_start = "┼"
            elif (
                next_block_start == " "
                and tile_pair_has_wall(r, c, Direction.WEST)
                and tile_pair_has_wall(r + 1, c, Direction.WEST)
            ):
                next_block_start = "├"
            elif tile_pair_has_wall(r + 1, c, Direction.WEST):
                next_block_start = "┌"
            elif tile_pair_has_wall(r, c, Direction.WEST):
                next_block_start = "└"
            next_line = next_block_start + HORIZONTAL * (CHAR_WIDTH - 1)
            next_block_start = HORIZONTAL
        else:
            if (
                next_block_start == HORIZONTAL
                and tile_pair_has_wall(r, c, Direction.WEST)
                and tile_pair_has_wall(r + 1, c, Direction.WEST)
            ):
                next_block_start = "┤"
            elif next_block_start == HORIZONTAL and tile_pair_has_wall(r + 1, c, Direction.WEST):
                next_block_start = "┐"
            elif next_block_start == HORIZONTAL and tile_pair_has_wall(r, c, Direction.WEST):
                next_block_start = "┘"
            elif tile_pair_has_wall(r, c, Direction.WEST) and tile_pair_has_wall(
                r + 1, c, Direction.WEST
            ):
                next_block_start = VERTICAL

            next_line = next_block_start + " " * (CHAR_WIDTH - 1)
            next_block_start = " "
        return next_line, next_block_start

    world_arr = [[Tile() for _ in range(world.num_avenues)] for _ in range(world.num_streets)]

    world_arr[world.num_streets - karel_street][karel_avenue - 1].value = "K"
    for (avenue, street), count in world.beepers.items():
        world_arr[world.num_streets - street][avenue - 1].beepers = count

    for wall in world.walls:
        avenue, street, direction = wall.avenue, wall.street, wall.direction
        world_arr[world.num_streets - street][avenue - 1].walls.append(direction)

    for r in range(1, world.num_streets + 1):
        for c in range(1, world.num_avenues + 1):
            if world.corner_color(c, r):
                world_arr[world.num_streets - r][c - 1].color = world.corner_color(c, r)

    result = f"┌{HORIZONTAL * (CHAR_WIDTH * world.num_avenues + 1)}┐\n"
    for r in range(world.num_streets):
        next_line = VERTICAL
        result += VERTICAL
        next_block_start = " "
        for c in range(world.num_avenues):
            tile = world_arr[r][c]
            line, next_block_start = get_next_line(r, c, next_block_start)
            next_line += line
            result += VERTICAL if tile_pair_has_wall(r, c, Direction.WEST) else " "
            result += str(tile)

        result += f" {VERTICAL}\n"
        if r == world.num_streets - 1:
            result += f"└{HORIZONTAL * (CHAR_WIDTH * world.num_avenues + 1)}┘\n"
        else:
            result += f"{next_line} {VERTICAL}\n"
    return result
