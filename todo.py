# Even though errors: Import "flask" could not be resolved, when starting the app with `flask --app flask_world run`, it works.
from flask import Flask, render_template, request
import random
import base64
import json

app = Flask(__name__)

todos = ["cut grass"]


@app.route("/")
def todo():
    return render_template("todo.html", todos=todos)


@app.route("/api/save", methods=["POST"])
def save():
    print(request.data)
    data = request.data.decode("utf-8")
    print(data)

    todos.append(str(data))
    todos.append(str(random.random()))
    return render_template("todo.html", todos=todos)


if __name__ == "__main__":
    app.run(debug=True)  # debug=True means live reload
