from flask import Flask, render_template, redirect
from todo import TodoList

app = Flask(__name__)
tl = TodoList("todo.list")

# Routes to administrative pages


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", todo_items=tl.getItems())


@app.route("/update/<id>", methods=["GET"])
def update_item(id):
    tl.update(id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True, threaded=True)
