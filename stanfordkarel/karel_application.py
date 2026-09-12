"""
This file defines the GUI for running Karel programs.

Original Author: Nicholas Bowman
Credits: Kylie Jue, Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
"""

from __future__ import annotations

import contextlib
import tkinter as tk
from pathlib import Path
from time import sleep
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showwarning
from typing import TYPE_CHECKING

from .karel_canvas import KarelCanvas
from .karel_constants import DEFAULT_ICON, LIGHT_GREY, PAD_X, PAD_Y

if TYPE_CHECKING:
    from .karel_program import KarelProgram

from .karel_executor import execute_student_program
from .student_code import StudentCode


class KarelApplication(tk.Frame):
    def __init__(
        self,
        karel: KarelProgram,
        code_file: Path,
        master: tk.Tk,
        window_width: int = 800,
        window_height: int = 600,
        canvas_width: int = 600,
        canvas_height: int = 400,
    ) -> None:
        # set window background to contrast white Karel canvas
        master.configure(background=LIGHT_GREY)

        # disable dark mode in macOS to maintain legibility (#8)
        with contextlib.suppress(tk.TclError):
            master.tk.call(
                "tk::unsupported::MacWindowStyle", "appearance", str(master), "aqua"
            )

        # configure location of canvas to expand to fit window resizing
        master.rowconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)

        # set master geometry
        master.geometry(f"{window_width}x{window_height}")

        super().__init__(master, background=LIGHT_GREY)

        self.karel = karel
        self.world = karel.world
        self.code_file = code_file
        self.load_student_code()
        master.title(self.student_code.module_name)
        self.icon = DEFAULT_ICON
        self.window_width = window_width
        self.window_height = window_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.master = master
        self.set_dock_icon()
        self.grid(row=0, column=0)
        self.create_menubar()
        self.create_canvas()
        self.create_buttons()
        self.create_slider()
        self.create_status_label()

    def load_student_code(self) -> None:
        self.student_code = StudentCode(self.code_file)

    def set_dock_icon(self) -> None:
        # make Karel dock icon image
        path = Path(__file__).absolute().parent / "icon.png"
        try:
            img = tk.Image("photo", file=path)
            self.master.tk.call("wm", "iconphoto", self.master._w, img)  # type: ignore[attr-defined] # noqa: SLF001
        except tk.TclError:
            print(f"Warning: invalid icon.png: {path}")

    def create_menubar(self) -> None:
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="Exit", underline=1, command=self.master.quit, accelerator="Cmd+W"
        )
        iconmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Select Icon", menu=iconmenu)
        iconmenu.add_command(label="Karel", command=lambda: self.set_icon("karel"))
        iconmenu.add_command(label="Simple", command=lambda: self.set_icon("simple"))

        self.bind_all("<Command-w>", lambda _: self.quit())
        self.master.config(menu=menubar)  # type: ignore[attr-defined]

    def create_slider(self) -> None:
        """
        This method creates a frame containing three widgets:
        two labels on either side of a scale slider to control
        Karel execution speed.
        """
        self.slider_frame = tk.Frame(self, bg=LIGHT_GREY)
        self.slider_frame.grid(row=3, column=0, padx=PAD_X, pady=PAD_Y, sticky="ew")

        self.fast_label = tk.Label(self.slider_frame, text="Fast", bg=LIGHT_GREY)
        self.fast_label.pack(side="right")

        self.slow_label = tk.Label(self.slider_frame, text="Slow", bg=LIGHT_GREY)
        self.slow_label.pack(side="left")

        self.speed = tk.DoubleVar()

        self.scale = tk.Scale(
            self.slider_frame,
            orient=tk.HORIZONTAL,
            variable=self.speed,
            showvalue=False,
        )
        self.scale.set(self.world.init_speed)
        self.scale.pack()

    def create_canvas(self) -> None:
        """This method creates the canvas on which Karel and the world are drawn."""
        self.canvas = KarelCanvas(
            self.canvas_width,
            self.canvas_height,
            self.master,
            world=self.world,
            karel=self.karel,
        )
        self.canvas.grid(column=1, row=0, sticky="NESW")
        self.canvas.bind("<Configure>", lambda _: self.canvas.redraw_all())

    def set_icon(self, icon: str) -> None:
        self.canvas.icon = icon
        self.canvas.redraw_karel()

    def create_buttons(self) -> None:
        """
        This method creates the three buttons that appear on the left
        side of the screen. These buttons control the start of Karel
        execution, resetting Karel's state, and loading new worlds.
        """
        self.program_control_button = tk.Button(
            self, highlightthickness=0, highlightbackground="white"
        )
        self.program_control_button["text"] = "Run Program"
        self.program_control_button["command"] = self.run_program
        self.program_control_button.grid(
            column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky="ew"
        )

        self.load_world_button = tk.Button(
            self, highlightthickness=0, text="Load World", command=self.load_world
        )
        self.load_world_button.grid(
            column=0, row=2, padx=PAD_X, pady=PAD_Y, sticky="ew"
        )

    def create_status_label(self) -> None:
        """This function creates the status label at the bottom of the window."""
        self.status_label = tk.Label(
            self.master, text="Welcome to Karel!", bg=LIGHT_GREY
        )
        self.status_label.grid(row=1, column=0, columnspan=2)

    def disable_buttons(self) -> None:
        self.program_control_button.configure(state="disabled")
        self.load_world_button.configure(state="disabled")

    def enable_buttons(self) -> None:
        self.program_control_button.configure(state="normal")
        self.load_world_button.configure(state="normal")

    def on_karel_action(self, action_name: str) -> None:
        _ = action_name  # unused
        self.canvas.redraw_all()
        self.update()
        sleep(1 - self.speed.get() / 100)

    def run_program(self) -> None:
        # reimport code in case it changed
        self.load_student_code()
        self.status_label.configure(text="Running...", fg="brown")
        self.disable_buttons()
        self.update()

        success = execute_student_program(
            self.student_code, self.karel, self.on_karel_action
        )

        if success:
            self.status_label.configure(text="Finished running.", fg="green")
        else:
            # Let the user know their program crashed
            self.status_label.configure(
                text="Program crashed, check console for details.", fg="red"
            )
            self.update()
            showwarning(
                "Karel Error", "Karel Crashed!\nCheck the terminal for more details."
            )

        # Update program control button to force user
        # to reset world before running program again
        self.program_control_button["text"] = "Reset World"
        self.program_control_button["command"] = self.reset_world
        self.enable_buttons()

    def reset_world(self) -> None:
        self.karel.reset_state()
        self.world.reset_world()
        self.canvas.redraw_all()
        self.status_label.configure(text="Reset to initial state.", fg="black")
        # Once world has been reset, program control button resets to "run" mode
        self.program_control_button["text"] = "Run Program"
        self.program_control_button["command"] = self.run_program
        self.update()

    def load_world(self) -> None:
        default_worlds_path = Path(__file__).absolute().parent / "worlds"
        filename = askopenfilename(
            initialdir=default_worlds_path,
            title="Select Karel World",
            filetypes=[("Karel Worlds", "*.w")],
            parent=self.master,
        )
        # User hit cancel and did not select file, so leave world as-is
        if not filename:
            return
        self.world.reload_world(filename=filename)
        self.karel.reset_state()
        self.canvas.redraw_all()
        # Reset speed slider
        self.scale.set(self.world.init_speed)
        self.status_label.configure(
            text=f"Loaded world from {Path(filename).name}.", fg="black"
        )

        # Make sure program control button is set to 'run' mode
        self.program_control_button["text"] = "Run Program"
        self.program_control_button["command"] = self.run_program
