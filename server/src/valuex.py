
# -*- coding: utf-8 -*-

import random

from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder = "../../public/static", template_folder = "../../public")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    return "Hello " + name + "!"

@app.route("/random")
def get_random():
    response = { "randomNumber" : random.randint(1, 100) }
    return jsonify(response)

@app.route("/", defaults = {"path" : ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080)
