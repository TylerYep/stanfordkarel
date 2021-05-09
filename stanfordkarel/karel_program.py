"""
This file defines the KarelProgram class, which provides the actual
implementation of all functions described in the Karel Reference
Guide.

All instances of a Karel object store a reference to the world
in which they exist. Each Karel object exists on a given
(avenue, street) intersection and holds a certain number of beepers
in its beeper bag.


Original Author: Nicholas Bowman
Credits: Kylie Jue, Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
"""
from __future__ import annotations

from .karel_ascii import AsciiKarelWorld, compare_output
from .karel_world import COLOR_MAP, INFINITY, Direction, KarelWorld

NEXT_DIRECTION_MAP = {
    Direction.NORTH: Direction.WEST,
    Direction.WEST: Direction.SOUTH,
    Direction.SOUTH: Direction.EAST,
    Direction.EAST: Direction.NORTH,
}
NEXT_DIRECTION_MAP_RIGHT = {v: k for k, v in NEXT_DIRECTION_MAP.items()}

# This map associates directions with the delta that Karel
# undergoes if it were to move one step in that direction
# delta is in terms of (avenue, street)
DIRECTION_DELTA_MAP = {
    Direction.NORTH: (0, 1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, -1),
    Direction.WEST: (-1, 0),
}


class KarelProgram:
    def __init__(self, world_file: str) -> None:
        """
        This functions instantiates a new Karel instance and sets its
        location and current number of beepers to be the default starting
        values as indicated by the given world object.

        Parameters:
            world (KarelWorld) - The world that Karel should exists in

        Members:
            avenue (int) - The current avenue Karel is standing on.
            street (int) - The current street Karel is standing on.
            street (Direction[Enum]) - The current direction Karel is facing.
            num_beepers (int) - The current number of beepers Karel has.

        Returns: None
        """
        self.world = KarelWorld(world_file)
        self.avenue, self.street = self.world.karel_start_location
        self.direction = self.world.karel_start_direction
        self.num_beepers = self.world.karel_start_beeper_count

    def __repr__(self) -> str:
        """Creates a Karel World in ASCII Art!"""
        return str(AsciiKarelWorld(self.world, self.street, self.avenue))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, KarelProgram):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def compare_with(self, other: KarelProgram, two_columns: bool = True) -> bool:
        """
        Options:
            two_columns: bool (default=True)
        """
        if self == other:
            return True
        if not two_columns:
            print(f"\n\nStudent output:\n{self}")
            print(f"\nExpected output:\n{other}")
            return False

        print(compare_output(self, other))
        return False

    def reset_state(self) -> None:
        """
        This function is used to reset Karel's location and direction to the original
        starting parameters as indicated by the world that Karel lives in.

        Parameters: None
        Returns: None
        """
        self.avenue, self.street = self.world.karel_start_location
        self.direction = self.world.karel_start_direction
        self.num_beepers = self.world.karel_start_beeper_count

    def move(self) -> None:
        """
        This function moves Karel forward one space in the direction that it is
        currently facing. If Karel's front is not clear (blocked by wall or boundary
        of world) then a KarelException will be raised).

        Parameters: None
        Returns: None
        """
        if not self.front_is_clear():
            raise KarelException(
                self.avenue,
                self.street,
                self.direction,
                "Karel attempted to move, but its front was blocked.",
            )

        delta_avenue, delta_street = DIRECTION_DELTA_MAP[self.direction]
        self.avenue += delta_avenue
        self.street += delta_street

    def turn_left(self) -> None:
        """
        This function turns Karel 90 degrees counterclockwise.

        Parameters: None
        Returns: None
        """
        self.direction = NEXT_DIRECTION_MAP[self.direction]

    def put_beeper(self) -> None:
        """
        This function places a beeper on the corner that Karel is currently standing
        on and decreases Karel's beeper count by 1. If Karel has no more beepers in its
        beeper bag, then this function raises a KarelException.

        Parameters: None
        Returns: None
        """
        if self.num_beepers == 0:
            raise KarelException(
                self.avenue,
                self.street,
                self.direction,
                "Karel attempted to put a beeper, but it had none left in its bag.",
            )

        if self.num_beepers != INFINITY:
            self.num_beepers -= 1

        self.world.add_beeper(self.avenue, self.street)

    def pick_beeper(self) -> None:
        """
        This function removes a beeper from the corner that Karel is currently
        standing on and increases Karel's beeper count by 1. If there are no beepers
        on Karel's current corner, then this function raises a KarelException.

        Parameters: None
        Returns: None
        """
        if not self.beepers_present():
            raise KarelException(
                self.avenue,
                self.street,
                self.direction,
                "Karel attempted to pick up a beeper, "
                "but there were none on the current corner.",
            )

        if self.num_beepers != INFINITY:
            self.num_beepers += 1

        self.world.remove_beeper(self.avenue, self.street)

    def front_is_clear(self) -> bool:
        """
        This function returns a boolean indicating whether or not there is a wall
        in front of Karel.

        Parameters: None
        Returns:
            is_clear (Bool) - True if there is no wall in front of Karel
                              False otherwise
        """
        return self.direction_is_clear(self.direction)

    def direction_is_clear(self, direction: Direction) -> bool:
        """
        This is a helper function that returns a boolean indicating whether
        or not there is a barrier in the specified direction of Karel.

        Parameters:
            direction (Direction[Enum]) - The direction in which to check for a barrier

        Returns:
            is_clear (Bool) - True if there is no barrier in the specified direction
                              False otherwise
        """
        delta_avenue, delta_street = DIRECTION_DELTA_MAP[direction]
        next_avenue = self.avenue + delta_avenue
        next_street = self.street + delta_street

        # front is not clear if we are about to go out of bounds
        if not self.world.in_bounds(next_avenue, next_street):
            return False

        # front is not clear if wall exists in same direction we're currently facing
        if self.world.wall_exists(self.avenue, self.street, direction):
            return False

        # must also check for alternate possible representation of wall
        opposite_direction = NEXT_DIRECTION_MAP[NEXT_DIRECTION_MAP[direction]]
        if self.world.wall_exists(next_avenue, next_street, opposite_direction):
            return False

        # If all previous conditions checked out, then the front is clear
        return True

    def front_is_blocked(self) -> bool:
        """
        This function returns a boolean indicating whether there is a wall
        in front of Karel.

        Parameters: None
        Returns:
            is_blocked (Bool) - True if there is a wall in front of Karel
                                  False otherwise
        """
        return not self.front_is_clear()

    def left_is_clear(self) -> bool:
        """
        This function returns a boolean indicating whether or not there is a wall
        to the left of Karel.

        Parameters: None
        Returns:
            is_clear (Bool) - True if there is no wall to the left of Karel
                              False otherwise
        """
        return self.direction_is_clear(NEXT_DIRECTION_MAP[self.direction])

    def left_is_blocked(self) -> bool:
        """
        This function returns a boolean indicating whether there is a wall
        to the left of Karel.

        Parameters: None
        Returns:
            is_blocked (Bool) - True if there is a wall to the left of Karel
                                  False otherwise
        """
        return not self.left_is_clear()

    def right_is_clear(self) -> bool:
        """
        This function returns a boolean indicating whether or not there is a wall
        to the right of Karel.

        Parameters: None
        Returns:
            is_clear (Bool) - True if there is no wall to the right of Karel
                              False otherwise
        """
        return self.direction_is_clear(NEXT_DIRECTION_MAP_RIGHT[self.direction])

    def right_is_blocked(self) -> bool:
        """
        This function returns a boolean indicating whether there is a wall
        to the right of Karel.

        Parameters: None
        Returns:
            is_blocked (Bool) - True if there is a wall to the right of Karel
                                  False otherwise
        """
        return not self.right_is_clear()

    def beepers_present(self) -> bool:
        """
        This function returns a boolean indicating whether or not there is
        a beeper on Karel's current corner.

        Parameters: None
        Returns:
            beepers_on_corner (Bool) - True if there's at least one beeper
                                       on Karel's current corner, False otherwise
        """
        return self.world.beepers[(self.avenue, self.street)] != 0

    def no_beepers_present(self) -> bool:
        return not self.beepers_present()

    def beepers_in_bag(self) -> bool:
        """
        This function returns a boolean indicating whether or not there is
        at least one beeper in Karel's beeper bag.

        Parameters: None
        Returns:
            beepers_in_bag (Bool) - True if there is at least one beeper in Karel's bag
                                    False otherwise
        """
        # Can't check > 0 because INFINITY beepers is -1
        return self.num_beepers != 0

    def no_beepers_in_bag(self) -> bool:
        # Only 0 beepers in bag indicates empty bag – negative represents INFINITY
        return self.num_beepers == 0

    def facing_north(self) -> bool:
        """
        This function returns a boolean indicating whether or not Karel is currently
        facing North.

        Parameters: None
        Returns:
            facing_north (Bool) - True if Karel is currently facing North
                                  False otherwise
        """
        return self.direction == Direction.NORTH

    def not_facing_north(self) -> bool:
        return not self.facing_north()

    def facing_east(self) -> bool:
        """
        This function returns a boolean indicating whether or not Karel is currently
        facing East.

        Parameters: None
        Returns:
            facing_east (Bool) - True if Karel is currently facing East
                                 False otherwise
        """
        return self.direction == Direction.EAST

    def not_facing_east(self) -> bool:
        return not self.facing_east()

    def facing_west(self) -> bool:
        """
        This function returns a boolean indicating whether or not Karel is currently
        facing West.

        Parameters: None
        Returns:
            facing_west (Bool) - True if Karel is currently facing West
                                 False otherwise
        """
        return self.direction == Direction.WEST

    def not_facing_west(self) -> bool:
        return not self.facing_west()

    def facing_south(self) -> bool:
        """
        This function returns a boolean indicating whether or not Karel is currently
        facing South.

        Parameters: None
        Returns:
            facing_south (Bool) - True if Karel is currently facing South
                                  False otherwise
        """
        return self.direction == Direction.SOUTH

    def not_facing_south(self) -> bool:
        return not self.facing_south()

    def paint_corner(self, color: str) -> None:
        """
        This function makes Karel paint its current corner the indicated color.
        This function will raise a KarelException if the indicated color is not one
        of the valid predefined colors. For this list of colors, check the
        kareldefinitions.py file.

        Parameters:
            color (str) - The color string specifying which color to paint the corner
        Returns: None
        """
        if color is not None and color not in COLOR_MAP:
            raise KarelException(
                self.avenue,
                self.street,
                self.direction,
                f"Karel attempted to paint the corner with color {color}, "
                "which is not valid.",
            )
        self.world.paint_corner(self.avenue, self.street, color)

    def corner_color_is(self, color: str) -> bool:
        """
        This function returns a boolean indicating whether or not Karel's current
        corner is the specified color.

        Parameters:
            color (str) - Color string representing the color to
            check the current corner for
        Returns:
            is_color (Bool) - True if Karel's current corner is the specified color
                              False otherwise
        """
        return self.world.corner_color(self.avenue, self.street) == color


class KarelException(Exception):
    """The following classes define Karel-specific exceptions."""

    def __init__(
        self, avenue: int, street: int, direction: Direction, message: str
    ) -> None:
        super().__init__()
        self.avenue = avenue
        self.street = street
        self.direction = direction.value.capitalize()
        self.message = message

    def __str__(self) -> str:
        return (
            f"Karel crashed while on avenue {self.avenue} and street {self.street}, "
            f"facing {self.direction}\nInvalid action: {self.message}"
        )
