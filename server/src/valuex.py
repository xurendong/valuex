
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
import flask_restful
from flask_restful import reqparse # 直接用 flask_restful.reqparse.RequestParser() 会报 reqparse 不存在

import config

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

app = flask.Flask(__name__, static_folder = "../../public/static", template_folder = "../../public")
app.response_class = Response_CORS
app.config.from_object(config.config["config_d"])
app.config["upload_path"] = "I:\\Project\\Project\\ValueX\\public\\upload" # 必须绝对路径？

api = flask_restful.Api(app)

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/hello")
def hello():
    name = flask.request.args.get("name", "")
    return "Hello " + name + "!"

@app.route("/random")
def get_random():
    response = { "randomNumber": random.randint(1, 100) }
    return flask.jsonify(response)

@app.route("/upload_file", methods=["GET", "POST"])
def upload_file():
    if flask.request.method == "POST":
        for f in flask.request.files.getlist("file"):
            f.save(os.path.join(app.config["upload_path"], f.filename))
    return flask.render_template("index.html")

@app.route("/", defaults = {"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return flask.render_template("index.html")

task_to_do = {
    "task_1": {"task": "build an API"},
    "task_2": {"task": "啦啦啦啦啦"},
    "task_3": {"task": "profit!"},
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
        task_id = "task_%d" % (len(task_to_do.keys()) + 1)
        task_to_do[task_id] = {"task": args["workname"]}
        return task_to_do[task_id], 201

class Restful_TaskID(flask_restful.Resource):
    def get(self, task_id):
        abort_if_task_not_exist(task_id)
        return task_to_do[task_id]

    def delete(self, task_id):
        abort_if_task_not_exist(task_id)
        del task_to_do[task_id]
        return "", 204

    def put(self, task_id):
        abort_if_task_not_exist(task_id) # 不存在不自动添加
        args = parser.parse_args()
        task = {"task": args["workname"]}
        task_to_do[task_id] = task
        return task, 201

api.add_resource(Restful, "/restful")
api.add_resource(Restful_TaskID, "/restful/<task_id>")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080)
