"""
This file defines the KarelImageRenderer class, which is responsible for
rendering a Karel world into a Pillow Image object. This is used for
creating animated GIFs of a Karel program's execution.
Author: Gemini Code Assist
"""

from __future__ import annotations

import io
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw, ImageFont

from .karel_constants import (
    BORDER_OFFSET,
    DEFAULT_ICON,
)
from .karel_executor import execute_student_program
from .karel_renderer import KarelBaseRenderer

if TYPE_CHECKING:
    from .karel_program import KarelProgram
    from .karel_world import KarelWorld
    from .student_code import StudentCode

try:
    from IPython.display import Image as IPythonImage  # type: ignore[import-not-found]
    from IPython.display import display
except ImportError:
    IPythonImage = None
    display = None


class KarelImageRenderer(KarelBaseRenderer):
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont
    beeper_font: ImageFont.FreeTypeFont | ImageFont.ImageFont
    image_width: int
    image_height: int
    draw: ImageDraw.ImageDraw

    def __init__(
        self, world: KarelWorld, karel: KarelProgram, cell_size: int = 50
    ) -> None:
        super().__init__(world, karel)
        self.cell_size = cell_size
        self.icon = DEFAULT_ICON
        self.init_geometry_values()
        try:
            self.font = ImageFont.truetype("arial.ttf", 10)
            self.beeper_font = ImageFont.truetype("arial.ttf", 12)
        except OSError:
            self.font = ImageFont.load_default()
            self.beeper_font = ImageFont.load_default()

    def init_geometry_values(self) -> None:
        """Calculate image dimensions based on world size."""
        self.boundary_width = self.cell_size * self.world.num_avenues
        self.boundary_height = self.cell_size * self.world.num_streets

        self.image_width = int(self.boundary_width + 2 * BORDER_OFFSET)
        self.image_height = int(self.boundary_height + 2 * BORDER_OFFSET)

        self.left_x = BORDER_OFFSET
        self.top_y = BORDER_OFFSET
        self.right_x = self.left_x + self.boundary_width
        self.bottom_y = self.top_y + self.boundary_height

    def render_frame(self) -> Image.Image:
        """Render the current world state to a Pillow Image object."""
        image = Image.new("RGB", (self.image_width, self.image_height), "white")
        self.draw = ImageDraw.Draw(image)

        self.draw_world()
        self.draw_karel()

        return image

    def draw_line(self, points: list[float], fill: str, width: int, tag: str) -> None:
        _ = tag  # unused
        self.draw.line(points, fill=fill, width=width)

    def draw_polygon(
        self,
        points: list[float],
        fill: str,
        outline: str,
        width: int,
        tag: str,
    ) -> None:
        _ = tag  # unused
        if len(outline) == 0:
            outline = fill  # use fill color if no outline specified
        self.draw.polygon(points, fill=fill, outline=outline, width=width)

    def draw_text(
        self,
        location: tuple[float, float],
        text: str,
        fill: str,
        font: str,
        anchor: str,
        tag: str,
    ) -> None:
        _ = tag  # unused
        font_obj = self.beeper_font if font == "Arial 12" else self.font
        self.draw.text(location, text, fill=fill, font=font_obj, anchor=anchor)

    def run_and_render_to_gif(
        self,
        student_code: StudentCode,
    ) -> None:
        """
        Run Karel headlessly and render the output as a GIF.
        This requires the Pillow library.
        """
        success, frames = self._run_and_collect_frames(student_code)

        if frames:
            output_filename = f"{student_code.module_name}.gif"
            # Duration is inverse of speed (slider is 0-100)
            duration = int(1000 * (1 - self.world.init_speed / 100))
            frames[0].save(
                output_filename,
                save_all=True,
                append_images=frames[1:],
                duration=max(50, duration),
                loop=0,
            )
            print(f"Karel animation saved to {output_filename}")
            if not success:
                print(
                    "\nWarning: The program crashed. The saved GIF may be incomplete."
                )

    def _run_and_collect_frames(
        self, student_code: StudentCode
    ) -> tuple[bool, list[Image.Image]]:
        """
        Run the student's program and collect image frames for each action.

        Returns a tuple of (success, frames).
        """
        frames = [self.render_frame()]  # Capture initial state

        def on_action(_action_name: str) -> None:
            frames.append(self.render_frame())

        success = execute_student_program(student_code, self.karel, on_action)
        return success, frames

    def run_and_render_to_ipython(
        self,
        student_code: StudentCode,
    ) -> None:
        """
        Run Karel headlessly and render the output as a GIF in an IPython environment.
        This requires the Pillow and IPython libraries.
        """
        if IPythonImage is None or display is None:
            print("IPython is not installed. Cannot display animation.")
            return

        success, frames = self._run_and_collect_frames(student_code)

        if frames:
            duration = int(1000 * (1 - self.world.init_speed / 100))
            with io.BytesIO() as buffer:
                frames[0].save(
                    buffer,
                    "GIF",
                    save_all=True,
                    append_images=frames[1:],
                    duration=max(50, duration),
                    loop=0,
                )
                display(IPythonImage(data=buffer.getvalue()))

        if not success:
            print(
                "\nWarning: The program crashed. The displayed GIF may be incomplete."
            )
