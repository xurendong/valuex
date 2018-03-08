
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

import time

import pymysql as MySQLdb

from warnings import filterwarnings
filterwarnings("error", category = MySQLdb.Warning)

try: import logger
except: pass

class DBM_MySQL():
    def __init__(self, **kwargs):
        self.logText = ""
        self.logCate = "DBM_MySQL"
        self.logShow = "V"
        self.logInst = None
        try: self.logInst = logger.Logger()
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

    def SendMessage(self, logType, logCate, logInfo):
        if self.logInst != None:
            self.logInst.SendMessage(logType, logCate, logInfo, self.logShow)
        else:
            print("%s：%s：%s" % (logType, logCate, logInfo))

    def Connect(self):
        self.Disconnect()
        try:
            self.connect = MySQLdb.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset = self.charset)
            return True
        except MySQLdb.Warning as w:
            self.connect = None
            self.logText = "连接警告：%s" % str(w)
            self.SendMessage("W", self.logCate, self.logText)
        except MySQLdb.Error as e:
            self.connect = None
            self.logText = "连接错误：%d:%s" % (e.args[0], e.args[1].decode("utf-8"))
            self.SendMessage("E", self.logCate, self.logText)
        return False

    def Disconnect(self):
        if self.connect != None:
            self.connect.close()
            self.connect = None

    def CheckConnect(self):
        tryTimes = 0
        notConnect = True
        while notConnect == True and tryTimes < 1000:
            try:
                self.connect.ping()
                notConnect = False #说明连接正常
            except:
                self.logText = "检测到数据库连接已断开！"
                self.SendMessage("W", self.logCate, self.logText)
                if self.Connect() == True: #重连成功
                    notConnect = False #连接已经正常
                    self.logText = "数据库重连成功。"
                    self.SendMessage("I", self.logCate, self.logText)
                    break
                else:
                    tryTimes += 1
                    self.logText = "数据库重连失败！%d" % tryTimes
                    self.SendMessage("W", self.logCate, self.logText)
                    time.sleep(5) #等待重试

    def ExecuteSql(self, sql):
        if self.connect == None:
            self.logText = "执行(单)错误：数据库尚未连接！"
            self.SendMessage("W", self.logCate, self.logText)
            return False
        else:
            try:
                self.CheckConnect()
                self.cursor = self.connect.cursor()
                self.cursor.execute(sql)
                self.connect.commit() #
                self.cursor.close()
                return True
            except MySQLdb.Warning as w:
                self.logText = "执行(单)警告：%s" % str(w)
                self.SendMessage("W", self.logCate, self.logText)
            except MySQLdb.Error as e:
                self.logText = "执行(单)错误：%d:%s" % (e.args[0], e.args[1].decode("utf-8"))
                self.SendMessage("E", self.logCate, self.logText)
            return False

    def ExecuteManySql(self, sql, values):
        if self.connect == None:
            self.logText = "执行(多)错误：数据库尚未连接！"
            self.SendMessage("W", self.logCate, self.logText)
            return False
        else:
            try:
                self.CheckConnect()
                self.cursor = self.connect.cursor()
                self.cursor.executemany(sql, values)
                self.connect.commit() #
                self.cursor.close()
                return True
            except MySQLdb.Warning as w:
                self.logText = "执行(多)警告：%s" % str(w)
                self.SendMessage("W", self.logCate, self.logText)
            except MySQLdb.Error as e:
                self.logText = "执行(多)错误：%d:%s" % (e.args[0], e.args[1].decode("utf-8"))
                self.SendMessage("E", self.logCate, self.logText)
            return False

    def QueryAllSql(self, sql):
        if self.connect == None:
            self.logText = "查询(全)错误：数据库尚未连接！"
            self.SendMessage("W", self.logCate, self.logText)
            return None
        else:
            try:
                self.CheckConnect()
                self.cursor = self.connect.cursor()
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                self.cursor.close()
                return result
            except MySQLdb.Warning as w:
                self.logText = "查询(全)警告：%s" % str(w)
                self.SendMessage("W", self.logCate, self.logText)
            except MySQLdb.Error as e:
                self.logText = "查询(全)错误：%d:%s" % (e.args[0], e.args[1].decode("utf-8"))
                self.SendMessage("E", self.logCate, self.logText)
            return None
