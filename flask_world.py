# Even though errors: Import "flask" could not be resolved, when starting the app with `flask --app flask_world run`, it works.
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, <a href='/page/222'>World!</a></p>"


@app.route("/page/<int:number>")
def page(number):
    return f"<p>Page {number}....</p>"


if __name__ == "__main__":
    app.run(debug=True)  # debug=True means live reload
