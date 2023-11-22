# To create virtual environment
Virtual environment is basically an environment to store requirements aka dependencies locally, not globally.
  `python -m venv <name of environment>`
This creates my-venv folder.

To activate virtual environment,
  `<name of environment>\Scripts\activate.bat`

Terminal should show `(<name of environment>)` to the left.

To deactive
  `deactivate`

# To save dependencies
  `pip install <name of dependency>`

  `pip freeze > requirements.txt`

To remove,
  `pip uninstall <name of dependency>`