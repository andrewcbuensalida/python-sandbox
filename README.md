# To create virtual environment
Virtual environment is basically an environment to store requirements aka dependencies locally, not globally.
  `python -m venv <name of environment>`
If in wsl
  `python3 -m venv <name of environment>`
This creates my-venv folder.

To activate virtual environment, (remove .bat if in pycharm)
  `<name of environment>\Scripts\activate.bat`
If in wsl
  `source <name of environment>/bin/activate`

Terminal should show `(<name of environment>)` to the left.

To deactive
  `deactivate`

# To save dependencies
One at a time
  `pip install <name of dependency>`

  `pip freeze > requirements.txt`

If installing all dependencies from requirements.txt
  `pip install -r requirements.txt`

To remove,
  `pip uninstall <name of dependency>`

# Using the play button on the top right of the file uses global dependencies. Better to run the file in the command prompt with python <file.py> so you know it will use dependencies in virtual env.

# Work in pycharm because cmd in vs code won't stop spider.py's recursive requests


# If gitignore is not working
  `git rm -rf --cached .`
  `git add .`

