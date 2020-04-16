from karel.stanfordkarel import *


def turn_right():
    turn_left()
    turn_left()
    turn_left()


def turn_around():
    turn_left()
    turn_left()


def go_to_newspaper():
    move()
    move()
    turn_right()
    move()
    turn_left()
    move()


def collect_newspaper():
    pick_beeper()


def return_home():
    turn_around()
    move()
    turn_right()
    move()
    turn_left()
    move()
    move()
    turn_around()


def main():
    go_to_newspaper()
    collect_newspaper()
    return_home()


if __name__ == "__main__":
    run_karel_program()
