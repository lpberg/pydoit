from flask import Flask, flash, jsonify, render_template, request, redirect
from todo import TodoList
from datetime import datetime
import sys
import os
import json

app = Flask(__name__)
tl = TodoList("todo.list")

# Routes to administrative pages

@app.route('/', methods=['GET'])
def index():
	return render_template(
		"index.html",
		todo_items = tl.getItems()
	)

@app.route('/update/<id>', methods=['GET'])
def update_item(id):
	tl.update(id)
	return redirect('/')

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5006, debug=True, threaded=True)
