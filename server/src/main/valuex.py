
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

import flask
import flask_cors
import flask_restful
import flask_socketio
from flask_restful import reqparse

import config

# -------------------------------------------------- #

app = flask.Flask(__name__, static_folder = "../../../public/static", template_folder = "../../../public")
app.config.from_object(config.config["config_d"])
app.config["upload_path"] = "I:\\Project\\Project\\ValueX\\public\\upload" # 必须绝对路径？

flask_cors.CORS(app, supports_credentials = True)

api = flask_restful.Api(app)
socketio = flask_socketio.SocketIO(app)

# -------------------------------------------------- #

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/upload_file", methods=["GET", "POST"])
def upload_file():
    if flask.request.method == "POST":
        for f in flask.request.files.getlist("file"):
            f.save(os.path.join(app.config["upload_path"], f.filename))
    response = { "status": 1, "message": "upload success!" }
    return flask.jsonify(response)

@app.route("/", defaults = {"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return flask.render_template("index.html")

# -------------------------------------------------- #

@socketio.on("connect", namespace = "/test_sio")
def test_connect():
    flask_socketio.emit("my_response", {"data": "connected"})
    print("client connect")

@socketio.on("disconnect", namespace = "/test_sio")
def test_disconnect():
    print("client disconnect")

# -------------------------------------------------- #

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", port = 8080) # 使用 Apache 等，无法使用 WebSocket 协议
    socketio.run(app, host = "0.0.0.0", port = 8080) # 使用 eventlet 或 gevent 甚至 gunicorn 等，可以使用 WebSocket 协议
