
# -*- coding: utf-8 -*-

# Copyright (c) 2018-2018 the ValueX authors
# All rights reserved.
#
# The project sponsor and lead author is Xu Rendong.
# E-mail: xrd@ustc.edu, QQ: 277195007, WeChat: ustc_xrd
# You can get more information at https://xurendong.github.io
# For names of other contributors see the contributors file.
#
# Commercial use of this code in source and binary forms is
# governed by a LGPL v3 license. You may get a copy from the
# root directory. Or else you should get a specific written 
# permission from the project author.
#
# Individual and educational use of this code in source and
# binary forms is governed by a 3-clause BSD license. You may
# get a copy from the root directory. Certainly welcome you
# to contribute code of all sorts.
#
# Be sure to retain the above copyright notice and conditions.

import os
import random

from flask import Flask, render_template, request, jsonify

import config

app = Flask(__name__, static_folder = "../../public/static", template_folder = "../../public")
app.config.from_object(config.config["config_d"])
app.config["upload_path"] = "I:\\Project\\Project\\ValueX\\public\\upload" # 必须绝对路径？

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

@app.route("/upload_file", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        for f in request.files.getlist("file"):
            f.save(os.path.join(app.config["upload_path"], f.filename))
    return render_template("index.html")

@app.route("/", defaults = {"path" : ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080)
