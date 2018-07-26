
# -*- coding: utf-8 -*-

# Copyright (c) 2018-2018 the ValueX authors
# All rights reserved.
#
# The project sponsor and lead author is Xu Rendong.
# E-mail: xrd@ustc.edu, QQ: 277195007, WeChat: ustc_xrd
# See the contributors file for names of other contributors.
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
import assess

# -------------------------------------------------- #

upload_path = "I:\\Project\\Project\\ValueX\\public\\upload" # 必须绝对路径？
public_folder = "../../../public"
template_folder = public_folder
static_folder = public_folder + "/static"
report_folder = public_folder + "/report"

app = flask.Flask(__name__, static_folder = static_folder, template_folder = template_folder)
app.config.from_object(config.config["config_d"])
app.config["upload_path"] = upload_path

flask_cors.CORS(app, supports_credentials = True)

api = flask_restful.Api(app)
socketio = flask_socketio.SocketIO(app)

# -------------------------------------------------- #

@app.route("/")
def index():
    return flask.render_template("/index.html")

@app.route("/upload_file", methods=["GET", "POST"])
def upload_file():
    response = { "status": 0, "message": "upload & save failed!" }
    if flask.request.method == "POST":
        assesser = assess.Assess()
        for f in flask.request.files.getlist("file"):
            save_path = os.path.join(app.config["upload_path"], f.filename)
            f.save(save_path)
            ret = assesser.SaveUploadData(save_path)
            if ret == True:
                response = { "status": 1, "message": "upload & save success." }
    return flask.jsonify(response)

@app.route("/make_report")
def make_report():
    response = { "status": 0, "message": "make report failed!" }
    assesser = assess.Assess()
    result = assesser.GetDailyReport("LHTZ_20170428001", 20170101, 20180228)
    if not result.empty:
        #print(result)
        ret = assesser.StrategyEvaluation(result)
        if ret == True:
            ret = assesser.ExportResultReport()
            if ret == True:
                response = { "status": 1, "message": "make report success." }
    return flask.jsonify(response)

@app.route("/check_report")
def check_report():
    file_path = public_folder + "/report/report.html"
    response = { "status": 0, "message": "check report failed!" }
    if os.path.exists(file_path):
        response = { "status": 1, "message": "check report success." }
    return flask.jsonify(response)

@app.route("/view_report")
def view_report():
    file_path = "/report/report.html"
    return flask.render_template(file_path)

@app.route("/", defaults = {"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return flask.render_template("/index.html")

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
    data_folder = "../data" # 数据文件夹
    temp_folder = "../temp" # 模板文件夹
    #rets_folder = "../rets" # 结果文件夹
    rets_folder = report_folder # 结果文件夹
    assesser = assess.Assess() # 作为单件全局初始化
    assesser.InitAssess(data_folder = data_folder, temp_folder = temp_folder, rets_folder = rets_folder) # 不使用数据库
    #assesser.InitAssess(host = "10.0.7.53", port = 3306, user = "root", passwd = "root", data_folder = data_folder, temp_folder = temp_folder, rets_folder = rets_folder)
    #app.run(host = "0.0.0.0", port = 8080) # 使用 Apache 等，无法使用 WebSocket 协议
    socketio.run(app, host = "0.0.0.0", port = 8080) # 使用 eventlet 或 gevent 甚至 gunicorn 等，可以使用 WebSocket 协议
