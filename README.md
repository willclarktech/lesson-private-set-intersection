# Lesson: Private Set Intersection

This repository is a supplement to the private set intersection lesson from [OpenMined’s](https://www.openmined.org/) [Foundations of Private Computation course](https://courses.openmined.org/courses/foundations-of-private-computation).
The source text for some of the modules in that lesson can be found in `./text/`. A code exercise for one of the modules is in `./code/` and is also hosted on repl.it:

-   https://repl.it/@willclarktech/PSIExercise
-   https://repl.it/@willclarktech/PSISolution

It’s probably easiest for you to complete the coding exercises on repl.it, but this repository is here in case you prefer to work locally.

## Setup

This repository assumes you are using Python v3.8 or above. I recommend you work in a virtual environment of some kind.

The easiest way to install dependencies is using [poetry](https://python-poetry.org/), which will also manage virtual environments for you. Simply run

```sh
poetry install
```

then activate the virtual environment by running

```sh
poetry shell
```

If you aren’t using poetry, you can install the dependencies via the `requirements.txt` file in the usual way. For example using pip:

```sh
pip install -r requirements.txt
```

Once you’ve installed the dependencies, you should be able to run the tests and see that they fail:

```sh
pytest
```

## Coding exercise

Your task is to fill out the functionality for the interfaces defined in `./code/private_set_intersection.py`. You can run the tests against your code by running `pytest`.

Be aware that the test is just a simple check that you’re heading in the right direction, it’s not supposed to be particularly robust. Write more tests if you find it helpful!

If you get stuck, try going back to the course content, or if you’re really stuck then take a look at the solution file.

## Useful scripts

Run these from the root directory:

-   Typechecking: `mypy code`
-   Running tests: `pytest`
-   Linting: `pylint code/private_set_intersection.py code/test_private_set_intersection.py`
-   Formatting code: `black code`
