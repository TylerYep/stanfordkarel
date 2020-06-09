"""
This file defines the class definition of a Karel world.

The sub header comment defines important notes about the Karel
world file format.

General Notes About World Construction
- Streets run EAST-WEST (rows)
- Avenues run NORTH-SOUTH (columns)

World File Constraints:
- World file should specify one component per line in the format
  KEYWORD: PARAMETERS
- Any lines with no colon delimiter will be ignored
- The accepted KEYWORD, PARAMETER combinations are as follows:
    - Dimension: (num_avenues, num_streets)
    - Wall: (avenue, street); direction
    - Beeper: (avenue, street) count
    - Karel: (avenue, street); direction
    - Color: (avenue, street); color
    - Speed: delay
    - BeeperBag: num_beepers
- Multiple parameter values for the same keyword should be separated by a semicolon
- All numerical values (except delay) must be expressed as ints. The exception
  to this is that the number of beepers can also be INFINITY
- Any specified color values must be valid TKinter color strings, and are limited
  to the set of colors
- Direction is case-insensitive and can be one of the following values:
    - East
    - West
    - North
    - South

Original Author: Nicholas Bowman
Credits: Kylie Jue, Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
Last Modified: 3/31/2020
"""
import collections
import copy
import os
import re
import sys

from .karel_definitions import (
    COLOR_MAP,
    DIRECTIONS_MAP,
    DIRECTIONS_MAP_INVERSE,
    INFINITY,
    Direction,
    Wall,
)

INIT_SPEED = 50
VALID_WORLD_KEYWORDS = ["dimension", "wall", "beeper", "karel", "speed", "beeperbag", "color"]
KEYWORD_DELIM = ":"
PARAM_DELIM = ";"
DEFAULT_WORLD_FILE = "default_world.w"


class KarelWorld:
    def __init__(self, world_file=None):
        """
        Karel World constructor
        Parameters:
            world_file: filename of world file containing the initial state of Karel's world
        """
        self.world_name = world_file
        self._world_file = self.process_world(world_file) if world_file else None

        # Map of beeper locations to the count of beepers at that location
        self._beepers = collections.defaultdict(int)

        # Map of corner colors, defaults to None
        self._corner_colors = collections.defaultdict(lambda: "")

        # Set of Wall objects placed in the world
        self._walls = set()

        # Dimensions of the world
        self._num_streets = 1
        self._num_avenues = 1

        # Initial Karel state saved to enable world reset
        self._karel_starting_location = (1, 1)
        self._karel_starting_direction = Direction.EAST
        self._karel_starting_beeper_count = 0

        # Initial speed slider setting
        self._init_speed = INIT_SPEED

        # If a world file has been specified, load world details from the file
        if self._world_file:
            self.load_from_file()

        # Save initial beeper state to enable world reset
        self._init_beepers = copy.deepcopy(self._beepers)

    def __eq__(self, other):
        return (
            self.beepers == other.beepers
            and self.walls == other.walls
            and self.num_streets == other.num_streets
            and self.num_avenues == other.num_avenues
            and self.corner_colors == other.corner_colors
        )

    @staticmethod
    def process_world(world_file, worlds_path="worlds"):
        # Find world file that matches program name in the worlds/ directory
        no_worlds_folder = False
        worlds_prefix = os.path.join(worlds_path, world_file + ".w")
        if not os.path.isfile(worlds_prefix):
            worlds_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "worlds")
            worlds_prefix = os.path.join(worlds_path, world_file + ".w")
            if not os.path.isdir(worlds_path):
                no_worlds_folder = True

        if os.path.isfile(worlds_prefix):
            # First look inside the worlds folder for this file
            world_file = open(worlds_prefix)
        elif os.path.isfile(world_file):
            # Attempt to open the exact filename that has been specified
            world_file = open(world_file)
        elif no_worlds_folder:
            default_world = os.path.join(worlds_path, DEFAULT_WORLD_FILE)
            print(f"Could not find world file: {world_file}.w. Using default world instead.")
            print(worlds_path)
            if os.path.isfile(default_world):
                world_file = open(default_world)
            else:
                sys.tracebacklimit = 0
                raise FileNotFoundError(
                    "Could not find default world to use. Please specify a valid world filename."
                )
        else:
            print(worlds_path)
            sys.tracebacklimit = 0
            raise FileNotFoundError(
                "Could not find worlds/ folder, and the specified file was not one of "
                "the provided worlds.\nPlease store custom worlds in a folder named worlds/, "
                "or use a world listed below:\n"
                + "\n".join([(" " * 4) + world for world in sorted(os.listdir(worlds_path))])
                + "\n\nSet the default world by using the name in run_karel_program().\n"
                "    e.g. run_karel_program('checkerboard_karel')"
            )

        return world_file

    @property
    def karel_starting_location(self):
        return self._karel_starting_location

    @property
    def karel_starting_direction(self):
        return self._karel_starting_direction

    @property
    def karel_starting_beeper_count(self):
        return self._karel_starting_beeper_count

    @property
    def init_speed(self):
        return self._init_speed

    @property
    def num_streets(self):
        return self._num_streets

    @num_streets.setter
    def num_streets(self, val):
        self._num_streets = val

    @property
    def num_avenues(self):
        return self._num_avenues

    @num_avenues.setter
    def num_avenues(self, val):
        self._num_avenues = val

    @property
    def beepers(self):
        return self._beepers

    @property
    def corner_colors(self):
        return self._corner_colors

    @property
    def walls(self):
        return self._walls

    def load_from_file(self):
        def parse_parameters(keyword, param_str):
            params = {}
            for param in param_str.split(PARAM_DELIM):
                param = param.strip()

                # check to see if parameter encodes a location
                coordinate = re.match(r"\((\d+),\s*(\d+)\)", param)
                if coordinate:
                    # avenue, street
                    params["location"] = (int(coordinate.group(1)), int(coordinate.group(2)))
                    continue

                # check to see if the parameter is a direction value
                if param in DIRECTIONS_MAP:
                    params["direction"] = DIRECTIONS_MAP[param]

                # check to see if parameter encodes a numerical value or color string
                elif keyword == "color":
                    if param.title() not in COLOR_MAP:
                        raise ValueError(f"Error: {param} is invalid parameter for {keyword}.")
                    params["color"] = param.title()

                # handle the edge case where Karel has infinite beepers
                elif param in ("infinity", "infinite") and keyword == "beeperbag":
                    params["val"] = INFINITY

                # float values are only valid for the speed parameter.
                elif keyword == "speed":
                    try:
                        params["val"] = int(100 * float(param))
                    except ValueError:
                        raise ValueError(f"Error: {param} is invalid parameter for {keyword}.")

                # must be a digit then
                elif param.isdigit():
                    params["val"] = int(param)

                else:
                    raise ValueError(f"Error: {param} is invalid parameter for {keyword}.")

            return params

        for i, line in enumerate(self._world_file):
            # Ignore blank lines and lines with no comma delineator
            line = line.strip()
            if not line:
                continue

            if ":" not in line:
                print(f"Incorrectly formatted line - ignoring line {i} of world file: {line}")
                continue

            keyword, param_str = line.lower().split(KEYWORD_DELIM)

            # only accept valid keywords as defined in world file spec
            # TODO: add error detection for keywords with insufficient parameters
            params = parse_parameters(keyword, param_str)

            # handle all different possible keyword cases
            if keyword == "dimension":
                # set world dimensions based on location values
                self._num_avenues, self._num_streets = params["location"]

            elif keyword == "wall":
                # build a wall at the specified location
                (avenue, street), direction = params["location"], params["direction"]
                self._walls.add(Wall(avenue, street, direction))

            elif keyword == "beeper":
                # add the specified number of beepers to the world
                self._beepers[params["location"]] += params["val"]

            elif keyword == "karel":
                # Give Karel initial state values
                self._karel_starting_location = params["location"]
                self._karel_starting_direction = params["direction"]

            elif keyword == "beeperbag":
                # Set Karel's initial beeper bag count
                self._karel_starting_beeper_count = params["val"]

            elif keyword == "speed":
                # Set delay speed of program execution
                self._init_speed = params["val"]

            elif keyword == "color":
                # Set corner color to be specified color
                self._corner_colors[params["location"]] = params["color"]

            else:
                print(f"Invalid keyword - ignoring line {i} of world file: {line}")

    def add_beeper(self, avenue, street):
        self._beepers[(avenue, street)] += 1

    def remove_beeper(self, avenue, street):
        if self._beepers[(avenue, street)] == 0:
            return
        self._beepers[(avenue, street)] -= 1

    def add_wall(self, wall):
        alt_wall = self.get_alt_wall(wall)
        if wall not in self._walls and alt_wall not in self._walls:
            self._walls.add(wall)

    def remove_wall(self, wall):
        alt_wall = self.get_alt_wall(wall)
        if wall in self._walls:
            self._walls.remove(wall)
        if alt_wall in self._walls:
            self._walls.remove(alt_wall)

    @staticmethod
    def get_alt_wall(wall):
        if wall.direction == Direction.NORTH:
            return Wall(wall.avenue, wall.street + 1, Direction.SOUTH)
        if wall.direction == Direction.SOUTH:
            return Wall(wall.avenue, wall.street - 1, Direction.NORTH)
        if wall.direction == Direction.EAST:
            return Wall(wall.avenue + 1, wall.street, Direction.WEST)
        if wall.direction == Direction.WEST:
            return Wall(wall.avenue - 1, wall.street, Direction.EAST)
        raise ValueError

    def paint_corner(self, avenue, street, color):
        self._corner_colors[(avenue, street)] = color

    def corner_color(self, avenue, street):
        return self._corner_colors[(avenue, street)]

    def reset_corner(self, avenue, street):
        self._beepers[(avenue, street)] = 0
        self._corner_colors[(avenue, street)] = ""

    def wall_exists(self, avenue, street, direction):
        wall = Wall(avenue, street, direction)
        return wall in self._walls

    def in_bounds(self, avenue, street):
        return 0 < avenue <= self._num_avenues and 0 < street <= self._num_streets

    def reset_world(self):
        """
        Reset initial state of beepers in the world
        """
        self._beepers = copy.deepcopy(self._init_beepers)
        self._corner_colors = collections.defaultdict(lambda: "")

    def reload_world(self, filename=None):
        """
        Reloads world using constructor.
        """
        self.__init__(filename)

    def save_to_file(self, filename, karel):
        with open(filename, "w") as f:
            # First, output dimensions of world
            f.write(f"Dimension: ({self.num_avenues}, {self.num_streets})\n")

            # Next, output all walls
            for wall in self._walls:
                f.write(
                    f"Wall: ({wall.avenue}, {wall.street}); "
                    f"{DIRECTIONS_MAP_INVERSE[wall.direction]}\n"
                )

            # Next, output all beepers
            for loc, count in self._beepers.items():
                f.write(f"Beeper: ({loc[0]}, {loc[1]}); {count}\n")

            # Next, output all color information
            for loc, color in self._corner_colors.items():
                if color:
                    f.write(f"Color: ({loc[0]}, {loc[1]}); {color}\n")

            # Next, output Karel information
            f.write(
                f"Karel: ({karel.avenue}, {karel.street}); "
                f"{DIRECTIONS_MAP_INVERSE[karel.direction]}\n"
            )

            # Finally, output beeperbag info
            beeper_output = karel.num_beepers if karel.num_beepers >= 0 else "INFINITY"
            f.write(f"BeeperBag: {beeper_output}\n")
