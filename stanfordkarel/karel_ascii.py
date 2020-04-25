from .karel_definitions import Direction

CHAR_WIDTH = 6
HORIZONTAL, VERTICAL = "─", "│"


class Tile:
    def __init__(self, value=""):
        self.value = value
        self.walls = []
        self.beepers = 0


def karel_ascii(world, karel_street, karel_avenue):
    """ Creates a Karel World in ASCII Art! """

    def tile_pair_has_wall(r, c, direction):
        """ Checks if the tile at r, c should have a wall by checking itself and its neighbors. """

        def tile_has_wall(r, c, direction):
            if r >= 0 and c >= 0 and r < world.num_streets and c < world.num_avenues:
                tile = world_arr[r][c]
                return direction in tile.walls
            return False

        if direction == Direction.SOUTH:
            return tile_has_wall(r, c, Direction.SOUTH) or tile_has_wall(r + 1, c, Direction.NORTH)
        elif direction == Direction.NORTH:
            return tile_has_wall(r, c, Direction.NORTH) or tile_has_wall(r - 1, c, Direction.SOUTH)
        elif direction == Direction.WEST:
            return tile_has_wall(r, c, Direction.WEST) or tile_has_wall(r, c - 1, Direction.EAST)
        elif direction == Direction.EAST:
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

    # TODO handle colors = world.corner_color(avenue, street)

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
