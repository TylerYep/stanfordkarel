from stanfordkarel.karel_definitions import Direction

CHAR_WIDTH = 6
HORIZONTAL, VERTICAL = "─", "│"


class Tile:
    def __init__(self, value=""):
        self.value = value
        self.walls = []
        self.beepers = 0


def karel_ascii(world, karel_street, karel_avenue):
    world_arr = [[Tile() for _ in range(world.num_avenues)] for _ in range(world.num_streets)]

    world_arr[world.num_streets - karel_street][karel_avenue - 1].value = "K"
    for (avenue, street), count in world.beepers.items():
        world_arr[world.num_streets - street][avenue - 1].beepers = count

    for wall in world.walls:
        avenue, street, direction = wall.avenue, wall.street, wall.direction
        world_arr[world.num_streets - street][avenue - 1].walls.append(direction)

    def _get_next_line(tile, r, c, next_block_start):
        tile_below = world_arr[r + 1][c] if r + 1 < world.num_streets else None
        if Direction.SOUTH in tile.walls:
            if (
                Direction.WEST in tile.walls
                and tile_below
                and Direction.WEST in tile_below.walls
                and next_block_start == HORIZONTAL
            ):
                next_block_start = "┼"
            elif (
                Direction.WEST in tile.walls
                and tile_below
                and Direction.WEST in tile_below.walls
                and next_block_start == " "
            ):
                next_block_start = "├"
            elif tile_below and Direction.WEST in tile_below.walls:
                next_block_start = "┌"
            elif Direction.WEST in tile.walls:
                next_block_start = "└"
            next_line = next_block_start + HORIZONTAL * (CHAR_WIDTH - 1)
            next_block_start = HORIZONTAL
        else:
            if (
                next_block_start == HORIZONTAL
                and Direction.WEST in tile.walls
                and tile_below
                and Direction.WEST in tile_below.walls
            ):
                next_block_start = " ┤"
            elif (
                next_block_start == HORIZONTAL and tile_below and Direction.WEST in tile_below.walls
            ):
                next_block_start = "┐"
            elif next_block_start == HORIZONTAL and Direction.WEST in tile.walls:
                next_block_start = "┘"
            elif Direction.WEST in tile.walls and tile_below and Direction.WEST in tile_below.walls:
                next_block_start = VERTICAL

            next_line = next_block_start + " " * (CHAR_WIDTH - 1)
            next_block_start = " "
        return next_line, next_block_start

    result = f"┌{HORIZONTAL * (CHAR_WIDTH * world.num_avenues + 1)}┐\n"
    for r in range(world.num_streets):
        next_line = VERTICAL
        result += VERTICAL
        next_block_start = " "
        for c in range(world.num_avenues):
            tile = world_arr[r][c]
            line, next_block_start = _get_next_line(tile, r, c, next_block_start)
            next_line += line
            result += VERTICAL if Direction.WEST in tile.walls else " "

            if tile.value == "K":
                result += " <K> " if tile.beepers > 0 else "  K  "
            elif tile.beepers > 0:
                result += f" <{tile.beepers}> "
            else:
                result += "  ·  "

        result += f" {VERTICAL}\n"
        if r == world.num_streets - 1:
            result += f"└{HORIZONTAL * (CHAR_WIDTH * world.num_avenues + 1)}┘\n"
        else:
            result += f"{next_line} {VERTICAL}\n"
    return result
