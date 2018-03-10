
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

# -*- coding: utf-8 -*-

import time

import pymysql

from warnings import filterwarnings
filterwarnings("error", category = pymysql.Warning)

try: import logger
except: pass

class DBM_MySQL():
    def __init__(self, **kwargs):
        self.log_text = ""
        self.log_cate = "DBM_MySQL"
        self.log_show = "V"
        self.log_inst = None
        try: self.log_inst = logger.Logger()
        except: pass
        self.host = kwargs.get("host", "0.0.0.0")
        self.port = kwargs.get("port", 0)
        self.user = kwargs.get("user", "user")
        self.passwd = kwargs.get("passwd", "123456")
        self.db = kwargs.get("db", "test")
        self.charset = kwargs.get("charset", "utf8")
        self.connect = None
        self.cursor = None

    def __del__(self):
        self.Disconnect()

    def SendMessage(self, log_type, log_cate, log_info):
        if self.log_inst != None:
            self.log_inst.SendMessage(log_type, log_cate, log_info, self.log_show)
        else:
            print("%s：%s：%s" % (log_type, log_cate, log_info))

    def Connect(self):
        self.Disconnect()
        try:
            self.connect = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset = self.charset)
            return True
        except pymysql.Warning as w:
            self.connect = None
            self.log_text = "连接警告：%s" % str(w)
            self.SendMessage("W", self.log_cate, self.log_text)
        except pymysql.Error as e:
            self.connect = None
            self.log_text = "连接错误：%d:%s" % (e.args[0], e.args[1].decode("utf-8"))
            self.SendMessage("E", self.log_cate, self.log_text)
        return False

    def Disconnect(self):
        if self.connect != None:
            self.connect.close()
            self.connect = None

    def CheckConnect(self):
        try_times = 0
        not_connect = True
        while not_connect == True and try_times < 1000:
            try:
                self.connect.ping()
                not_connect = False # 说明连接正常
            except:
                self.log_text = "检测到数据库连接已断开！"
                self.SendMessage("W", self.log_cate, self.log_text)
                if self.Connect() == True: # 重连成功
                    not_connect = False # 连接已经正常
                    self.log_text = "数据库重连成功。"
                    self.SendMessage("I", self.log_cate, self.log_text)
                    break
                else:
                    try_times += 1
                    self.log_text = "数据库重连失败！%d" % try_times
                    self.SendMessage("W", self.log_cate, self.log_text)
                    time.sleep(5) # 等待重试

    def ExecuteSql(self, sql):
        if self.connect == None:
            self.log_text = "执行(单)错误：数据库尚未连接！"
            self.SendMessage("W", self.log_cate, self.log_text)
            return False
        else:
            try:
                self.CheckConnect()
                self.cursor = self.connect.cursor()
                self.cursor.execute(sql)
                self.connect.commit() #
                self.cursor.close()
                return True
            except pymysql.Warning as w:
                self.log_text = "执行(单)警告：%s" % str(w)
                self.SendMessage("W", self.log_cate, self.log_text)
            except pymysql.Error as e:
                self.log_text = "执行(单)错误：%d:%s" % (e.args[0], e.args[1].decode("utf-8"))
                self.SendMessage("E", self.log_cate, self.log_text)
            return False

    def ExecuteManySql(self, sql, values):
        if self.connect == None:
            self.log_text = "执行(多)错误：数据库尚未连接！"
            self.SendMessage("W", self.log_cate, self.log_text)
            return False
        else:
            try:
                self.CheckConnect()
                self.cursor = self.connect.cursor()
                self.cursor.executemany(sql, values)
                self.connect.commit() #
                self.cursor.close()
                return True
            except pymysql.Warning as w:
                self.log_text = "执行(多)警告：%s" % str(w)
                self.SendMessage("W", self.log_cate, self.log_text)
            except pymysql.Error as e:
                self.log_text = "执行(多)错误：%d:%s" % (e.args[0], e.args[1].decode("utf-8"))
                self.SendMessage("E", self.log_cate, self.log_text)
            return False

    def QueryAllSql(self, sql):
        if self.connect == None:
            self.log_text = "查询(全)错误：数据库尚未连接！"
            self.SendMessage("W", self.log_cate, self.log_text)
            return None
        else:
            try:
                self.CheckConnect()
                self.cursor = self.connect.cursor()
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                self.cursor.close()
                return result
            except pymysql.Warning as w:
                self.log_text = "查询(全)警告：%s" % str(w)
                self.SendMessage("W", self.log_cate, self.log_text)
            except pymysql.Error as e:
                self.log_text = "查询(全)错误：%d:%s" % (e.args[0], e.args[1].decode("utf-8"))
                self.SendMessage("E", self.log_cate, self.log_text)
            return None
