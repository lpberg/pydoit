from flask import Flask, render_template, redirect
from todo import TodoList
from pathlib import Path

app = Flask(__name__)

tls = TodoList(Path("lists").joinpath("tasks.list"))


@app.route("/", methods=["GET"])
def index():
    return redirect("/tag/all")


@app.route("/tag/<tag_name>", methods=["GET"])
def tag(tag_name):
    return render_template(
        "index.html",
        tag_names=tls.getTags(),
        tag_name=tag_name,
        todo_items=tls.getItemsByTag(tag_name),
    )


@app.route("/update/<tag>/<id>", methods=["GET"])
def update_item(tag, id):
    tls.update(id)
    return redirect("/tag/" + tag)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True, threaded=True)
