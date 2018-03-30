
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

import flask
import werkzeug
import flask_cors
import flask_restful
import flask_socketio
from flask_restful import reqparse # 直接用 flask_restful.reqparse.RequestParser() 会报 reqparse 不存在

import config

# -------------------------------------------------- #

class Response_CORS(flask.Response):
    def __init__(self, response = None, **kwargs):
        allow_origin = ("Access-Control-Allow-Origin", "*")
        allow_methods = ("Access-Control-Allow-Methods", "HEAD, OPTIONS, GET, PUT, POST, DELETE")
        allow_headers = ("Access-Control-Allow-Headers", "Content-Type, Content-Length, Authorization, Accept, X-Requested-With, Referer, Origin, User-Agent")
        headers = kwargs.get("headers")
        if headers:
            headers.add(*allow_origin)
            headers.add(*allow_methods)
            headers.add(*allow_headers)
        else:
            headers = werkzeug.datastructures.Headers([allow_origin, allow_methods, allow_headers])
        kwargs["headers"] = headers
        super().__init__(response, **kwargs)

# -------------------------------------------------- #

app = flask.Flask(__name__, static_folder = "../../../public/static", template_folder = "../../../public")
# app.config["SECRET_KEY"] = "secret!"
app.config.from_object(config.config["config_d"])
app.config["upload_path"] = "I:\\Project\\Project\\ValueX\\public\\upload" # 必须绝对路径？

app.response_class = Response_CORS # 使用自定义 Response 解决跨域问题
# flask_cors.CORS(app, supports_credentials = True) # 使用 flask_cors 解决跨域问题

api = flask_restful.Api(app)
socketio = flask_socketio.SocketIO(app)

# -------------------------------------------------- #

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/hello")
def hello():
    name = flask.request.args.get("name", "")
    return "Hello " + name + "!"

@app.route("/random")
def get_random():
    response = { "random_number": random.randint(1, 100) }
    return flask.jsonify(response)

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

task_to_do = {
    1: {"task": "build an API"},
    2: {"task": "啦啦啦啦啦"},
    3: {"task": "profit!"},
}

parser = reqparse.RequestParser()
parser.add_argument("workname")

def abort_if_task_not_exist(task_id):
    if task_id not in task_to_do:
        flask_restful.abort(404, message="Task {} not exist".format(task_id))

class Restful(flask_restful.Resource):
    def get(self):
        return task_to_do

    def post(self):
        args = parser.parse_args()
        task_id = max(task_to_do.keys()) + 1
        task_to_do[task_id] = {"task": args["workname"]}
        return task_to_do[task_id], 201

class Restful_TaskID(flask_restful.Resource):
    def get(self, task_id):
        task_id = int(task_id)
        abort_if_task_not_exist(task_id)
        return task_to_do[task_id]

    def delete(self, task_id):
        task_id = int(task_id)
        abort_if_task_not_exist(task_id)
        del task_to_do[task_id]
        return "", 204

    def put(self, task_id):
        task_id = int(task_id)
        abort_if_task_not_exist(task_id) # 不存在不自动添加
        args = parser.parse_args()
        task = {"task": args["workname"]}
        task_to_do[task_id] = task
        return task, 201

api.add_resource(Restful, "/restful")
api.add_resource(Restful_TaskID, "/restful/<task_id>")

# -------------------------------------------------- #

@socketio.on("my_event", namespace = "/test_sio")
def test_message(message):
    flask_socketio.emit("my_response", {"data": message["msg"]})

@socketio.on("my_broadcast_event", namespace = "/test_sio")
def test_broadcast(message):
    flask_socketio.emit("my_response", {"data": message["msg"]}, broadcast = True)

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
