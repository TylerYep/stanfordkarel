# stanford-karel
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![PyPI version](https://badge.fury.io/py/stanfordkarel.svg)](https://badge.fury.io/py/stanfordkarel)
[![GitHub license](https://img.shields.io/github/license/TylerYep/stanford-karel)](https://github.com/TylerYep/stanford-karel/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/stanfordkarel)](https://pepy.tech/project/stanfordkarel)

This is a Python implementation of Karel for Stanford's CS 106A. This package is available on PyPI and allows you to run Karel programs without any additional setup!

Huge props to @nick-bowman for rewriting this project from scratch!

**StanfordKarel now supports:**
- Pip-installable package means you can run Karel programs from anywhere!
- Solution code no longer needed to grade assignments - instead, the output worlds are compared.
- Karel in ASCII! Plus autograder support.
- Improved autograding, testing, linting, and auto-formatting.


# Usage
`pip install stanfordkarel`

or

`git clone https://github.com/tyleryep/stanfordkarel.git`


# Documentation
## Running Karel
First, ensure that StanfordKarel is correctly installed using pip.
Any `.py` file can become a Karel program!

**collect_newspaper_karel.py**
```python
from stanfordkarel import *


def main():
    """ Karel code goes here! """
    turnLeft()
    move()
    turnLeft()


if __name__ == "__main__":
    run_karel_program()
```

Save the file and run:
```
python collect_newspaper_karel.py
```

![Karel Program](images/karel_program.png)


You can set a default world by passing a world name to run_karel_program, e.g. `run_karel_program("collect_newspaper_karel")`

### Folder structure
- `assignment1/`
    - `worlds/` (additional worlds go here)
        - `collect_newspaper_karel.w`
        - `collect_newspaper_karel_end.w`
    - `collect_newspaper_karel.py`


## Creating Worlds
If using the pip-installed version, simply run `python -m stanfordkarel.world_editor`.

To run the World Editor from the repository, simply run `python world_editor.py`.

![World Editor](images/world_editor.png)


## Grading
`./autograde` runs the available tests using pytest in the `tests/` folder and prints out any output differences in the world.
The tests use the student's code and the expected world output to determine correctness. If the output is not the same, the test driver will print out an ASCII representation of the differences.

![Autograder](images/autograder.png)


## Development
Everything important is located in `stanfordkarel/`.

- `stanfordkarel/` is the exported package, which contains all of the available functions and commands for students to use.
- `karel_application.py` is responsible for loading student code and displaying it to the screen.


# Contributing
All issues and pull requests are much appreciated! To run all tests and other auto-formatting tools, check out `scripts/run-tests`.


## Future Milestones
In the future, I hope to add:
- Automatic style checking
- Ways of determining the student's strategy or approach from observing Karel movements
- Autograde more worlds, broken down by assignment
- Allow students to autograde their own work
- Accessibility for visually-impaired students (using ascii karel)

### Minor TODOs
- Use f2string to convert all f strings to format strings for Python 3.5 compatibility
