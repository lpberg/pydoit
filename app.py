from flask import Flask, render_template, redirect
from todo import TodoList
from pathlib import Path

app = Flask(__name__)
tls = {}


def read_in_list_files():
    directory = Path("lists")
    for file_path in directory.iterdir():
        if file_path.is_file():
            if file_path.name.endswith(".list"):
                tls[file_path.stem] = TodoList(directory.joinpath(file_path.name))


read_in_list_files()


@app.route("/", methods=["GET"])
def root_redirect():
    return redirect("/" + next(iter(tls)))


@app.route("/<list_name>", methods=["GET"])
def index(list_name):
    return render_template(
        "index.html",
        list_names=tls.keys(),
        list_name=list_name,
        todo_items=tls[list_name].getItems(),
    )


@app.route("/update/<list_name>/<id>", methods=["GET"])
def update_item(list_name, id):
    tls[list_name].update(id)
    return redirect("/" + list_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True, threaded=True)
