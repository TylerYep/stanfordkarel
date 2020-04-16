from karel.stanfordkarel import *


def turn_right():
    turn_left()
    turn_left()
    turn_left()


def turn_around():
    turn_left()
    turn_left()


def draw_even_row():
    turn_right()
    put_beeper()
    while front_is_clear():
        move()
        if front_is_clear():
            move()
            put_beeper()
    turn_around()
    while front_is_clear():
        move()
    turn_right()


def draw_odd_row():
    turn_right()
    while front_is_clear():
        move()
        put_beeper()
        if front_is_clear():
            move()
    turn_around()
    while front_is_clear():
        move()
    turn_right()


def main():
    """
    Starts at the bottom left corner facing east.
    """
    turn_left()
    draw_even_row()
    while front_is_clear():
        move()
        draw_odd_row()
        if front_is_clear():
            move()
            draw_even_row()


if __name__ == "__main__":
    run_karel_program()
