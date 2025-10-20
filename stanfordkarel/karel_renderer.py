import cmath
import math
from abc import ABC, abstractmethod

from .karel_constants import (
    BEEPER_CELL_SIZE_FRAC,
    CORNER_SIZE,
    DEFAULT_ICON,
    DIRECTION_TO_RADIANS,
    KAREL_FOOT_LENGTH,
    KAREL_HEIGHT,
    KAREL_INNER_HEIGHT,
    KAREL_INNER_OFFSET,
    KAREL_INNER_WIDTH,
    KAREL_LEFT_HORIZONTAL_PAD,
    KAREL_LEG_FOOT_WIDTH,
    KAREL_LEG_HORIZONTAL_OFFSET,
    KAREL_LEG_LENGTH,
    KAREL_LEG_VERTICAL_OFFSET,
    KAREL_LINE_WIDTH,
    KAREL_LOWER_LEFT_DIAG,
    KAREL_MOUTH_HORIZONTAL_OFFSET,
    KAREL_MOUTH_VERTICAL_OFFSET,
    KAREL_MOUTH_WIDTH,
    KAREL_UPPER_RIGHT_DIAG,
    KAREL_VERTICAL_OFFSET,
    KAREL_WIDTH,
    LABEL_OFFSET,
    LINE_WIDTH,
    SIMPLE_KAREL_HEIGHT,
    SIMPLE_KAREL_WIDTH,
)
from .karel_program import KarelProgram
from .karel_world import COLOR_MAP, Direction, KarelWorld, Wall


class KarelBaseRenderer(ABC):
    def __init__(self, world: KarelWorld, karel: KarelProgram) -> None:
        self.world = world
        self.karel = karel
        self.icon = DEFAULT_ICON
        self.cell_size = 0.0
        self.left_x = 0.0
        self.top_y = 0.0
        self.right_x = 0.0
        self.bottom_y = 0.0
        self.boundary_width = 0.0
        self.boundary_height = 0.0

    @abstractmethod
    def draw_line(self, points: list[float], fill: str, width: int, tag: str) -> None:
        pass

    @abstractmethod
    def draw_polygon(
        self, points: list[float], fill: str, outline: str, width: int, tag: str
    ) -> None:
        pass

    @abstractmethod
    def draw_text(
        self,
        location: tuple[float, float],
        text: str,
        fill: str,
        font: str,
        anchor: str,
        tag: str,
    ) -> None:
        pass

    @abstractmethod
    def init_geometry_values(self) -> None:
        pass

    def draw_world(self) -> None:
        self.init_geometry_values()
        self._draw_corners()
        self._draw_all_beepers()
        self._draw_all_walls()
        self._draw_bounding_rectangle()
        self._label_axes()

    def _draw_bounding_rectangle(self) -> None:
        self.draw_line(
            [self.left_x, self.top_y, self.right_x, self.top_y],
            fill="black",
            width=LINE_WIDTH,
            tag="boundary",
        )
        self.draw_line(
            [self.left_x, self.top_y, self.left_x, self.bottom_y],
            fill="black",
            width=LINE_WIDTH,
            tag="boundary",
        )
        self.draw_line(
            [self.right_x, self.top_y, self.right_x, self.bottom_y],
            fill="black",
            width=LINE_WIDTH,
            tag="boundary",
        )
        self.draw_line(
            [self.left_x, self.bottom_y, self.right_x, self.bottom_y],
            fill="black",
            width=LINE_WIDTH,
            tag="boundary",
        )

    def _label_axes(self) -> None:
        for avenue in range(1, self.world.num_avenues + 1):
            label_x = self.calculate_corner_x(avenue)
            label_y = float(self.bottom_y + LABEL_OFFSET)
            self.draw_text(
                (label_x, label_y),
                str(avenue),
                fill="black",
                font="Arial 10",
                anchor="mt",
                tag="axis",
            )

        for street in range(1, self.world.num_streets + 1):
            label_x = self.left_x - LABEL_OFFSET
            label_y = self.calculate_corner_y(street)
            self.draw_text(
                (label_x, label_y),
                str(street),
                fill="black",
                font="Arial 10",
                anchor="rm",
                tag="axis",
            )

    def _draw_corners(self) -> None:
        for avenue in range(1, self.world.num_avenues + 1):
            for street in range(1, self.world.num_streets + 1):
                color = self.world.corner_color(avenue, street)
                corner_x = self.calculate_corner_x(avenue)
                corner_y = self.calculate_corner_y(street)
                if not color:
                    self.draw_line(
                        [
                            corner_x,
                            corner_y - CORNER_SIZE,
                            corner_x,
                            corner_y + CORNER_SIZE,
                        ],
                        fill="black",
                        width=1,
                        tag="corner",
                    )
                    self.draw_line(
                        [
                            corner_x - CORNER_SIZE,
                            corner_y,
                            corner_x + CORNER_SIZE,
                            corner_y,
                        ],
                        fill="black",
                        width=1,
                        tag="corner",
                    )
                else:
                    # self.create_rectangle(
                    #     corner_x - self.cell_size / 2,
                    #     corner_y - self.cell_size / 2,
                    #     corner_x + self.cell_size / 2,
                    #     corner_y + self.cell_size / 2,
                    #     fill=color,
                    #     tags="corner",
                    #     outline="",
                    # )
                    fill_color = COLOR_MAP.get(color, "black")
                    self.draw_polygon(
                        [
                            corner_x - self.cell_size / 2,
                            corner_y - self.cell_size / 2,
                            corner_x + self.cell_size / 2,
                            corner_y - self.cell_size / 2,
                            corner_x + self.cell_size / 2,
                            corner_y + self.cell_size / 2,
                            corner_x - self.cell_size / 2,
                            corner_y + self.cell_size / 2,
                        ],
                        fill=fill_color,
                        outline="",
                        width=1,
                        tag="corner",
                    )

    def _draw_all_beepers(self) -> None:
        for location, count in self.world.beepers.items():
            self._draw_beeper(location, count)

    def _draw_beeper(self, location: tuple[int, int], count: int) -> None:
        if count == 0:
            return

        corner_x = self.calculate_corner_x(location[0])
        corner_y = self.calculate_corner_y(location[1])
        beeper_radius = self.cell_size * BEEPER_CELL_SIZE_FRAC

        points = [
            corner_x,
            corner_y - beeper_radius,
            corner_x + beeper_radius,
            corner_y,
            corner_x,
            corner_y + beeper_radius,
            corner_x - beeper_radius,
            corner_y,
        ]
        self.draw_polygon(
            points, fill="lightgrey", outline="black", width=1, tag="beeper"
        )

        if count > 1:
            self.draw_text(
                (corner_x, corner_y),
                str(count),
                fill="black",
                font="Arial 12",
                anchor="mm",
                tag="beeper",
            )

    def _draw_all_walls(self) -> None:
        for wall in self.world.walls:
            self._draw_wall(wall)

    def _draw_wall(self, wall: Wall) -> None:
        avenue, street, direction = wall.avenue, wall.street, wall.direction
        corner_x = self.calculate_corner_x(avenue)
        corner_y = self.calculate_corner_y(street)
        cs_half = self.cell_size / 2

        if direction == Direction.NORTH:
            self.draw_line(
                [
                    corner_x - cs_half,
                    corner_y - cs_half,
                    corner_x + cs_half,
                    corner_y - cs_half,
                ],
                fill="black",
                width=LINE_WIDTH,
                tag="wall",
            )
        elif direction == Direction.SOUTH:
            self.draw_line(
                [
                    corner_x - cs_half,
                    corner_y + cs_half,
                    corner_x + cs_half,
                    corner_y + cs_half,
                ],
                fill="black",
                width=LINE_WIDTH,
                tag="wall",
            )
        elif direction == Direction.EAST:
            self.draw_line(
                [
                    corner_x + cs_half,
                    corner_y - cs_half,
                    corner_x + cs_half,
                    corner_y + cs_half,
                ],
                fill="black",
                width=LINE_WIDTH,
                tag="wall",
            )
        elif direction == Direction.WEST:
            self.draw_line(
                [
                    corner_x - cs_half,
                    corner_y - cs_half,
                    corner_x - cs_half,
                    corner_y + cs_half,
                ],
                fill="black",
                width=LINE_WIDTH,
                tag="wall",
            )

    def draw_karel(self) -> None:
        corner_x = self.calculate_corner_x(self.karel.avenue)
        corner_y = self.calculate_corner_y(self.karel.street)
        center = (corner_x, corner_y)
        angle = DIRECTION_TO_RADIANS[self.karel.direction]

        if self.icon == "karel":
            karel_origin_x = (
                corner_x
                - self.cell_size / 2
                + KAREL_LEFT_HORIZONTAL_PAD * self.cell_size
            )
            karel_origin_y = (
                corner_y - self.cell_size / 2 + KAREL_VERTICAL_OFFSET * self.cell_size
            )
            self._draw_karel_body(karel_origin_x, karel_origin_y, center, angle)
            self._draw_karel_legs(karel_origin_x, karel_origin_y, center, angle)
        elif self.icon == "simple":
            self._draw_simple_karel_icon(center, angle)

    @staticmethod
    def rotate_points(
        center: tuple[float, float], points: list[float], direction: float
    ) -> None:
        cangle = cmath.exp(direction * 1j)
        ccenter = complex(center[0], center[1])
        for i in range(0, len(points), 2):
            v = cangle * (complex(points[i], points[i + 1]) - ccenter) + ccenter
            points[i], points[i + 1] = v.real, v.imag

    def _draw_karel_body(
        self, x: float, y: float, center: tuple[float, float], direction: float
    ) -> None:
        width, height = self.cell_size * KAREL_WIDTH, self.cell_size * KAREL_HEIGHT
        lower_left_diag = (self.cell_size * KAREL_LOWER_LEFT_DIAG) / math.sqrt(2)
        upper_right_diag = (self.cell_size * KAREL_UPPER_RIGHT_DIAG) / math.sqrt(2)
        outer_points = [
            x,
            y,
            x + width - upper_right_diag,
            y,
            x + width,
            y + upper_right_diag,
            x + width,
            y + height,
            x + lower_left_diag,
            y + height,
            x,
            y + height - lower_left_diag,
        ]
        self.rotate_points(center, outer_points, direction)
        self.draw_polygon(
            outer_points,
            fill="white",
            outline="black",
            width=KAREL_LINE_WIDTH,
            tag="karel",
        )

        inner_x, inner_y = (
            x + self.cell_size * KAREL_INNER_OFFSET,
            y + self.cell_size * KAREL_INNER_OFFSET,
        )
        inner_width, inner_height = (
            self.cell_size * KAREL_INNER_WIDTH,
            self.cell_size * KAREL_INNER_HEIGHT,
        )
        inner_points = [
            inner_x,
            inner_y,
            inner_x + inner_width,
            inner_y,
            inner_x + inner_width,
            inner_y + inner_height,
            inner_x,
            inner_y + inner_height,
        ]
        self.rotate_points(center, inner_points, direction)
        self.draw_polygon(
            inner_points,
            fill="white",
            outline="black",
            width=KAREL_LINE_WIDTH,
            tag="karel",
        )

        mouth_x = x + self.cell_size * KAREL_MOUTH_HORIZONTAL_OFFSET
        mouth_y = inner_y + inner_height + self.cell_size * KAREL_MOUTH_VERTICAL_OFFSET
        mouth_width = self.cell_size * KAREL_MOUTH_WIDTH
        mouth_points = [mouth_x, mouth_y, mouth_x + mouth_width, mouth_y]
        self.rotate_points(center, mouth_points, direction)
        self.draw_line(mouth_points, fill="black", width=KAREL_LINE_WIDTH, tag="karel")

    def _draw_karel_legs(
        self, x: float, y: float, center: tuple[float, float], direction: float
    ) -> None:
        leg_len, foot_len, leg_foot_w = (
            self.cell_size * KAREL_LEG_LENGTH,
            self.cell_size * KAREL_FOOT_LENGTH,
            self.cell_size * KAREL_LEG_FOOT_WIDTH,
        )
        vert_off, horiz_off = (
            self.cell_size * KAREL_LEG_VERTICAL_OFFSET,
            self.cell_size * KAREL_LEG_HORIZONTAL_OFFSET,
        )

        left_leg = [
            x,
            y + vert_off,
            x - leg_len,
            y + vert_off,
            x - leg_len,
            y + vert_off + foot_len,
            x - leg_len + leg_foot_w,
            y + vert_off + foot_len,
            x - leg_len + leg_foot_w,
            y + vert_off + leg_foot_w,
            x,
            y + vert_off + leg_foot_w,
        ]
        self.rotate_points(center, left_leg, direction)
        self.draw_polygon(left_leg, fill="black", outline="black", width=1, tag="karel")

        y += self.cell_size * KAREL_HEIGHT
        right_leg = [
            x + horiz_off,
            y,
            x + horiz_off,
            y + leg_len,
            x + horiz_off + foot_len,
            y + leg_len,
            x + horiz_off + foot_len,
            y + leg_len - leg_foot_w,
            x + horiz_off + leg_foot_w,
            y + leg_len - leg_foot_w,
            x + horiz_off + leg_foot_w,
            y,
        ]
        self.rotate_points(center, right_leg, direction)
        self.draw_polygon(
            right_leg, fill="black", outline="black", width=1, tag="karel"
        )

    def _draw_simple_karel_icon(
        self, center: tuple[float, float], direction: float
    ) -> None:
        width, height = (
            self.cell_size * SIMPLE_KAREL_WIDTH,
            self.cell_size * SIMPLE_KAREL_HEIGHT,
        )
        center_x, center_y = center
        points = [
            center_x - width / 2,
            center_y - height / 2,
            center_x - width / 2,
            center_y + height / 2,
            center_x,
            center_y + height / 2,
            center_x + width / 2,
            center_y,
            center_x,
            center_y - height / 2,
        ]
        self.rotate_points(center, points, direction)
        self.draw_polygon(
            points, fill="white", outline="black", width=KAREL_LINE_WIDTH, tag="karel"
        )

    def calculate_corner_x(self, avenue: float) -> float:
        return self.left_x + self.cell_size / 2 + (avenue - 1) * self.cell_size

    def calculate_corner_y(self, street: float) -> float:
        return (
            self.top_y
            + self.cell_size / 2
            + (self.world.num_streets - street) * self.cell_size
        )
