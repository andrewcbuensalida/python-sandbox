# https://www.youtube.com/watch?v=XWuP5Yf5ILI&t=6130s
## Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment (mac/linux):

```bash
source .venv/bin/activate
```

For Windows
```bash
.venv\Scripts\activate.bat
```

In the future, to deactivate venv
```bash
.venv\Scripts\deactivate.bat 
```

## Install dependencies. This is not needed if doing a pip install in the notebook
`pip install -r requirements.txt`

## To save dependencies into requirements.txt
`pip freeze > requirements.txt`

# Using the play button on the top right of the file uses global dependencies. Better to run the file in the command prompt with python <file.py> so you know it will use dependencies in virtual env.

# Work in pycharm because cmd in vs code won't stop spider.py's recursive requests


# If gitignore is not working
  `git rm -rf --cached .`
  `git add .`

