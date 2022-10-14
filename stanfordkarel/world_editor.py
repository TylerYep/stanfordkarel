"""
This file defines the TK GUI for editing Karel worlds.

Original Author: Nicholas Bowman
Credits: Kylie Jue, Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
"""
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Any, Callable

from .karel_canvas import DEFAULT_ICON, LIGHT_GREY, PAD_X, PAD_Y, KarelCanvas
from .karel_program import KarelProgram
from .karel_world import COLOR_MAP, INFINITY, Direction

MIN_DIMENSIONS = 1
MAX_DIMENSIONS = 50
DEFAULT_COLOR = "Red"
DEFAULT_SIZE = 8


def run_world_editor() -> None:
    root = tk.Tk()
    world_builder = WorldBuilderApplication(master=root)
    world_builder.mainloop()


class WorldBuilderApplication(tk.Frame):
    def __init__(
        self,
        master: tk.Tk,
        window_width: int = 800,
        window_height: int = 400,
        canvas_width: int = 600,
        canvas_height: int = 400,
    ) -> None:
        # set window background to contrast white Karel canvas
        master.configure(background=LIGHT_GREY)

        # configure location of canvas to expand to fit window resizing
        master.rowconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.title("Karel World Builder")

        super().__init__(
            master, width=window_width, height=window_height, background=LIGHT_GREY
        )
        self.icon = DEFAULT_ICON
        self.window_width = window_width
        self.window_height = window_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.last_action_event_loc = (0.0, 0.0)
        self.master = master
        self.set_dock_icon()
        self.grid(row=0, column=0)
        self.master.update()
        self.setup_world()
        self.create_canvas()
        self.create_buttons()

    def set_dock_icon(self) -> None:
        # make Karel dock icon image
        path = Path(__file__).absolute().parent / "icon.png"
        try:
            img = tk.Image("photo", file=path)
            # pylint: disable=protected-access
            self.master.tk.call("wm", "iconphoto", self.master._w, img)  # type: ignore[attr-defined] # noqa: E501
        except tk.TclError:
            print(f"Warning: invalid icon.png: {path}")

    def setup_world(self) -> None:
        load_existing = messagebox.askyesno(
            "World Selection",
            "Would you like to load an existing world? \n\n"
            "Selecting 'No' will allow you to start with a blank slate.",
            parent=self.master,
        )
        if load_existing:
            self.load_world(init=True)
        else:
            self.create_new_world(init=True, default=True)

    def create_new_world(self, init: bool = False, default: bool = False) -> None:
        num_avenues = simpledialog.askinteger(
            "New World Size",
            "How many avenues should the new world have?",
            parent=self.master,
            minvalue=MIN_DIMENSIONS,
            maxvalue=MAX_DIMENSIONS,
        )

        if not num_avenues:
            if default:
                num_avenues = DEFAULT_SIZE
            else:
                # Cancel execution and return to existing world
                return

        num_streets = simpledialog.askinteger(
            "New World Size",
            "How many streets should the new world have?",
            parent=self.master,
            minvalue=MIN_DIMENSIONS,
            maxvalue=MAX_DIMENSIONS,
        )
        if not num_streets:
            if default:
                num_streets = DEFAULT_SIZE
            else:
                # Cancel execution and return to existing world
                return
        if init:
            self.karel = KarelProgram("")  # Use default world
            self.world = self.karel.world
        else:
            self.world.reload_world()
            self.karel.reset_state()

        self.world.num_avenues = num_avenues
        self.world.num_streets = num_streets
        if not init:
            self.canvas.redraw_all()

    def load_world(self, init: bool = False) -> None:
        default_worlds_path = Path(__file__).absolute().parent / "worlds"
        filename = askopenfilename(
            initialdir=default_worlds_path,
            title="Select Karel World",
            filetypes=[("Karel Worlds", "*.w")],
            parent=self.master,
        )
        # User hit cancel and did not select file, so leave world as-is
        if filename == "":
            if init:
                self.setup_world()
            return

        if init:
            self.karel = KarelProgram(filename)
            self.world = self.karel.world
        else:
            self.world.reload_world(filename)
            self.karel.reset_state()
            self.canvas.redraw_all()
            self.reset_direction_radio_buttons()
            self.reset_beeper_bag_radio_buttons()

    def create_canvas(self) -> None:
        """
        This method creates the canvas on which Karel and Karel's
        world are drawn.
        """
        self.canvas = KarelCanvas(
            self.canvas_width,
            self.canvas_height,
            self.master,
            world=self.world,
            karel=self.karel,
        )
        self.canvas.grid(column=1, row=0, sticky="NESW")
        self.canvas.bind("<Configure>", lambda t: self.canvas.redraw_all())
        self.canvas.bind("<Button-1>", self.handle_mouse_event)
        self.canvas.bind("<B1-Motion>", self.handle_mouse_event)

    def create_buttons(self) -> None:
        """
        This method creates the three buttons that appear on the left
        side of the screen. These buttons control the start of Karel
        execution, resetting Karel's state, and loading new worlds.
        """
        self.program_control_button = tk.Button(
            self, highlightthickness=0, highlightbackground="white"
        )
        self.program_control_button["text"] = "New World"
        self.program_control_button["command"] = self.create_new_world
        self.program_control_button.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y)

        self.load_world_button = tk.Button(
            self, highlightthickness=0, text="Load World", command=self.load_world
        )
        self.load_world_button.grid(column=0, row=1, padx=PAD_X, pady=PAD_Y)

        self.save_world_button = tk.Button(
            self, highlightthickness=0, text="Save World", command=self.save_world
        )
        self.save_world_button.grid(column=0, row=2, padx=PAD_X, pady=PAD_Y)

        self.create_direction_radio_buttons()
        self.create_beeper_bag_radio_buttons()
        self.create_action_radio_buttons()

    def create_direction_radio_buttons(self) -> None:
        self.dir_radio_frame = tk.Frame(self, bg=LIGHT_GREY)
        self.dir_radio_frame.grid(row=3, column=0, padx=PAD_X, pady=PAD_Y, sticky="ew")

        self.karel_direction_var = tk.StringVar()
        self.karel_direction_var.set(self.karel.direction.value)
        self.karel_direction_var.trace("w", self.update_karel_direction)

        dir_label = tk.Label(
            self.dir_radio_frame, text="Karel Direction: ", bg=LIGHT_GREY
        )
        dir_label.pack(side="left")
        tk.Radiobutton(
            self.dir_radio_frame,
            text="E",
            variable=self.karel_direction_var,
            value="east",
            bg=LIGHT_GREY,
        ).pack(side="left")
        tk.Radiobutton(
            self.dir_radio_frame,
            text="W",
            variable=self.karel_direction_var,
            value="west",
            bg=LIGHT_GREY,
        ).pack(side="left")
        tk.Radiobutton(
            self.dir_radio_frame,
            text="N",
            variable=self.karel_direction_var,
            value="north",
            bg=LIGHT_GREY,
        ).pack(side="left")
        tk.Radiobutton(
            self.dir_radio_frame,
            text="S",
            variable=self.karel_direction_var,
            value="south",
            bg=LIGHT_GREY,
        ).pack(side="left")

    def create_beeper_bag_radio_buttons(self) -> None:
        self.beeper_bag_radio_frame = tk.Frame(self, bg=LIGHT_GREY)
        self.beeper_bag_radio_frame.grid(
            row=4, column=0, padx=PAD_X, pady=PAD_Y, sticky="ew"
        )

        self.beeper_bag_var = tk.IntVar()
        self.beeper_bag_var.set(self.karel.num_beepers)
        self.beeper_bag_var.trace("w", self.update_karel_num_beepers)

        beeper_bag_label = tk.Label(
            self.beeper_bag_radio_frame, text="Beeper Bag: ", bg=LIGHT_GREY
        )
        beeper_bag_label.pack(side="left")
        tk.Radiobutton(
            self.beeper_bag_radio_frame,
            text="Empty",
            variable=self.beeper_bag_var,
            value=0,
            bg=LIGHT_GREY,
        ).pack(side="left")
        tk.Radiobutton(
            self.beeper_bag_radio_frame,
            text="Infinite",
            variable=self.beeper_bag_var,
            value=INFINITY,
            bg=LIGHT_GREY,
        ).pack(side="left")

    def create_action_radio_buttons(self) -> None:
        self.action_radio_frame = tk.Frame(self, bg=LIGHT_GREY)
        self.action_radio_frame.grid(
            row=5, column=0, padx=PAD_X, pady=PAD_Y, sticky="ew"
        )

        self.action_var = tk.StringVar()
        self.action_var.set("move_karel")

        action_label = tk.Label(self.action_radio_frame, text="Action: ", bg=LIGHT_GREY)
        action_label.pack(side="left")
        tk.Radiobutton(
            self.action_radio_frame,
            text="Move Karel",
            variable=self.action_var,
            value="move_karel",
            bg=LIGHT_GREY,
        ).pack(anchor="w")
        tk.Radiobutton(
            self.action_radio_frame,
            text="Add Wall",
            variable=self.action_var,
            value="add_wall",
            bg=LIGHT_GREY,
        ).pack(anchor="w")
        tk.Radiobutton(
            self.action_radio_frame,
            text="Remove Wall",
            variable=self.action_var,
            value="remove_wall",
            bg=LIGHT_GREY,
        ).pack(anchor="w")
        tk.Radiobutton(
            self.action_radio_frame,
            text="Add Beeper",
            variable=self.action_var,
            value="add_beeper",
            bg=LIGHT_GREY,
        ).pack(anchor="w")
        tk.Radiobutton(
            self.action_radio_frame,
            text="Remove Beeper",
            variable=self.action_var,
            value="remove_beeper",
            bg=LIGHT_GREY,
        ).pack(anchor="w")

        color_selection_frame = tk.Frame(self.action_radio_frame, bg=LIGHT_GREY)
        color_selection_frame.pack(anchor="w")

        self.color_var = tk.StringVar()
        self.color_var.set(DEFAULT_COLOR)

        tk.Radiobutton(
            color_selection_frame,
            text="Paint Corner",
            variable=self.action_var,
            value="paint_corner",
            bg=LIGHT_GREY,
        ).pack(side="left")
        self.color_dropdown = tk.OptionMenu(
            color_selection_frame, self.color_var, *sorted(COLOR_MAP)
        )
        self.color_dropdown["bg"] = LIGHT_GREY
        self.color_dropdown.pack(side="left")

        tk.Radiobutton(
            self.action_radio_frame,
            text="Reset Corner",
            variable=self.action_var,
            value="reset_corner",
            bg=LIGHT_GREY,
        ).pack(anchor="w")

    def reset_direction_radio_buttons(self) -> None:
        self.karel_direction_var.set(self.karel.direction.value)

    def reset_beeper_bag_radio_buttons(self) -> None:
        self.beeper_bag_var.set(self.karel.num_beepers)

    def update_karel_direction(self, *args: Any) -> None:
        del args
        new_dir = self.karel_direction_var.get()
        self.karel.direction = Direction(new_dir)
        self.canvas.redraw_karel()
        self.world.set_karel_start_direction(self.karel.direction)

    def update_karel_num_beepers(self, *args: Any) -> None:
        del args
        new_num_beepers = self.beeper_bag_var.get()
        self.karel.num_beepers = new_num_beepers
        self.world.set_karel_start_beeper_count(self.karel.num_beepers)

    def handle_mouse_event(self, event: tk.Event[Any]) -> None:
        def apply_function(fn: Callable[..., Any], *args: Any) -> None:
            if event_type is tk.EventType.ButtonPress:
                self.last_action_event_loc = (avenue, street)
                fn(avenue, street, *args)
                self.canvas.redraw_corners(update=False)
                self.canvas.redraw_beepers(update=False)
                self.canvas.redraw_walls(update=False)
                self.canvas.redraw_karel()

            elif event_type is tk.EventType.Motion:
                if (avenue, street) != self.last_action_event_loc:
                    self.last_action_event_loc = (avenue, street)
                    fn(avenue, street, *args)
                    self.canvas.redraw_corners(update=False)
                    self.canvas.redraw_beepers(update=False)
                    self.canvas.redraw_walls(update=False)
                    self.canvas.redraw_karel()

        event_type = event.type
        # only handle click events that happen in the world
        if not self.canvas.click_in_world(event.x, event.y):
            return

        avenue, street = self.canvas.calculate_location(event.x, event.y)
        avenue, street = int(avenue), int(street)
        action = self.action_var.get()
        if action == "move_karel":
            if avenue != self.karel.avenue or street != self.karel.street:
                self.karel.avenue = avenue
                self.karel.street = street
                self.canvas.redraw_karel()
                self.world.set_karel_start_location(avenue, street)
        elif action == "add_beeper":
            apply_function(self.world.add_beeper)
        elif action == "remove_beeper":
            apply_function(self.world.remove_beeper)
        elif action == "reset_corner":
            apply_function(self.world.reset_corner)
        elif action == "paint_corner":
            apply_function(self.world.paint_corner, self.color_var.get())
        elif action == "add_wall":
            wall = self.canvas.find_nearest_wall(event.x, event.y, avenue, street)
            if wall:
                self.world.add_wall(wall)
                self.canvas.redraw_walls()
        elif action == "remove_wall":
            wall = self.canvas.find_nearest_wall(event.x, event.y, avenue, street)
            if wall:
                self.world.remove_wall(wall)
                self.canvas.redraw_walls()

    def save_world(self) -> None:
        default_worlds_path = Path(__file__).absolute().parent / "worlds"
        filename = asksaveasfilename(
            initialdir=default_worlds_path,
            title="Save Karel World",
            filetypes=[("Karel Worlds", "*.w")],
            parent=self.master,
        )
        if filename == "":
            return
        if not filename.endswith(".w"):
            filename += ".w"
        self.world.save_to_file(Path(filename))


if __name__ == "__main__":
    run_world_editor()
