"""
This file defines the canvas upon which a Karel world is drawn. This
class defines all necessary methods to draw all components of a Karel
world, including walls, beepers, and Karel itself. All Karel applications
contains exactly one Karel Canvas object and each Karel Canvas object
holds information about one Karel World and one Karel object.

Original Author: Nicholas Bowman
Credits: Kylie Jue, Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
"""

from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

from .karel_constants import (
    BORDER_OFFSET,
    WALL_DETECTION_THRESHOLD,
)
from .karel_renderer import KarelBaseRenderer
from .karel_world import Direction, KarelWorld, Wall

if TYPE_CHECKING:
    from .karel_program import KarelProgram


class KarelCanvas(KarelBaseRenderer, tk.Canvas):
    def __init__(
        self,
        width: int,
        height: int,
        master: tk.Misc,
        world: KarelWorld,
        karel: KarelProgram,
        bg: str = "white",
    ) -> None:
        tk.Canvas.__init__(self, master, width=width, height=height, bg=bg)
        KarelBaseRenderer.__init__(self, world, karel)
        self.draw_world()
        self.draw_karel()

    def draw_line(self, points: list[float], fill: str, width: int, tag: str) -> None:
        self.create_line(*points, fill=fill, width=width, tags=tag)

    def draw_polygon(
        self,
        points: list[float],
        fill: str,
        outline: str,
        width: int,
        tag: str,
    ) -> None:
        self.create_polygon(*points, fill=fill, outline=outline, width=width, tags=tag)

    def draw_text(
        self,
        location: tuple[float, float],
        text: str,
        fill: str,
        font: str,
        anchor: str,
        tag: str,
    ) -> None:
        # anchor is not a valid parameter for create_text, so we ignore it
        # Additionally, the font parameter is a string like "Arial 10"
        # but create_text expects a tuple of (font_family, font_size)
        _ = anchor  # unused
        font_family, font_size = font.split()
        self.create_text(
            location, text=text, fill=fill, font=(font_family, int(font_size)), tags=tag
        )

    def redraw_all(self) -> None:
        self.delete("all")
        self.draw_world()
        self.draw_karel()
        self.update()

    def redraw_karel(self, update: bool = True) -> None:
        self.delete("karel")
        self.draw_karel()
        if update:
            self.update()

    def redraw_beepers(self, update: bool = True) -> None:
        self.delete("beeper")
        self._draw_all_beepers()
        if update:
            self.update()

    def redraw_corners(self, update: bool = True) -> None:
        self.delete("corner")
        self._draw_corners()
        if update:
            self.update()

    def redraw_walls(self, update: bool = True) -> None:
        self.delete("wall")
        self._draw_all_walls()
        if update:
            self.update()

    def init_geometry_values(self) -> None:
        self.update()

        horizontal_cell_size = (
            self.winfo_width() - 2 * BORDER_OFFSET
        ) / self.world.num_avenues
        vertical_cell_size = (
            self.winfo_height() - 2 * BORDER_OFFSET
        ) / self.world.num_streets

        self.cell_size = min(horizontal_cell_size, vertical_cell_size)

        self.boundary_height = self.cell_size * self.world.num_streets
        self.boundary_width = self.cell_size * self.world.num_avenues

        self.left_x = self.winfo_width() / 2 - self.boundary_width / 2
        self.top_y = self.winfo_height() / 2 - self.boundary_height / 2
        self.right_x = self.left_x + self.boundary_width
        self.bottom_y = self.top_y + self.boundary_height

    def click_in_world(self, x: float, y: float) -> bool:
        x = x - self.left_x
        y = y - self.top_y
        return 0 <= x < self.boundary_width and 0 <= y < self.boundary_height

    def calculate_location(self, x: float, y: float) -> tuple[float, float]:
        x = x - self.left_x
        y = y - self.top_y
        return (
            max(x, 0) // self.cell_size + 1,
            max((self.boundary_height - 1 - y), 0) // self.cell_size + 1,
        )

    def find_nearest_wall(
        self, x: float, y: float, avenue: int, street: int
    ) -> Wall | None:
        corner_x = self.calculate_corner_x(avenue)
        corner_y = self.calculate_corner_y(street)

        # distances to the four possible walls
        dist_to_east_wall = abs(x - (corner_x + self.cell_size / 2))
        dist_to_west_wall = abs(x - (corner_x - self.cell_size / 2))
        dist_to_south_wall = abs(y - (corner_y + self.cell_size / 2))
        dist_to_north_wall = abs(y - (corner_y - self.cell_size / 2))

        min_dist = min(
            dist_to_east_wall,
            dist_to_west_wall,
            dist_to_south_wall,
            dist_to_north_wall,
        )

        if min_dist > self.cell_size * WALL_DETECTION_THRESHOLD:
            return None

        if min_dist == dist_to_east_wall:
            return Wall(avenue, street, Direction.EAST)
        if min_dist == dist_to_west_wall:
            return Wall(avenue, street, Direction.WEST)
        if min_dist == dist_to_south_wall:
            return Wall(avenue, street, Direction.SOUTH)
        if min_dist == dist_to_north_wall:
            return Wall(avenue, street, Direction.NORTH)

        return None

    def add_wall_at_location(self, x: float, y: float) -> None:
        """Finds the nearest wall to a canvas click and adds it to the world."""
        avenue, street = self.calculate_location(x, y)
        wall = self.find_nearest_wall(x, y, int(avenue), int(street))
        if wall:
            self.world.add_wall(wall)

    def remove_wall_at_location(self, x: float, y: float) -> None:
        """Finds the nearest wall to a canvas click and removes it from the world."""
        avenue, street = self.calculate_location(x, y)
        wall = self.find_nearest_wall(x, y, int(avenue), int(street))
        if wall:
            self.world.remove_wall(wall)
