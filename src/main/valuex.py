
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

import os
import datetime

import numpy as np
import pandas as pd

try: import logger
except: pass
import dbm_mysql

class ValueX():
    def __init__(self):
        self.log_text = ""
        self.log_cate = "ValueX"
        self.log_show = "V"
        self.log_inst = None
        try: self.log_inst = logger.Logger()
        except: pass

    def __del__(self):
        pass

    def SendMessage(self, log_type, log_cate, log_info):
        if self.log_inst != None:
            self.log_inst.SendMessage(log_type, log_cate, log_info, self.log_show)
        else:
            print("%s：%s：%s" % (log_type, log_cate, log_info))

    def InitValueX(self, **kwargs):
        self.host = kwargs.get("host", "0.0.0.0")
        self.port = kwargs.get("port", 0)
        self.user = kwargs.get("user", "user")
        self.passwd = kwargs.get("passwd", "123456")
        self.charset = "utf8"
        self.folder = kwargs.get("folder", "") # 数据文件缓存
        self.db_clearx = "clearx"
        self.tb_daily_report = "daily_report"
        
        self.flag_use_database = True
        if self.host == "0.0.0.0": # 不使用数据库
            self.flag_use_database = False
        
        self.folder_clearx = ""
        if self.folder != "":
            self.folder_clearx = self.folder + "/clearx"
            if not os.path.exists(self.folder_clearx):
                os.makedirs(self.folder_clearx)
        
        self.dbm_clearx = None
        if self.flag_use_database == True:
            self.dbm_clearx = dbm_mysql.DBM_MySQL(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db_clearx, charset = self.charset) # db_clearx
            if self.dbm_clearx.Connect() == True:
                self.SendMessage("I", self.log_cate, "清算数据库连接完成。")
                return True
            else:
                self.SendMessage("E", self.log_cate, "清算数据库连接失败！")
                return False
        
        return True

    def TransDateIntToStr(self, int_date):
        year = int(int_date / 10000)
        month = int((int_date % 10000) / 100)
        day = int_date % 100
        return "%d-%d-%d" % (year, month, day)

    def GetTableModifyTime(self, dbm, db_name, tb_name):
        modify_time = None
        sql = "SELECT CREATE_TIME, UPDATE_TIME " + \
              "FROM information_schema.TABLES " + \
              "WHERE TABLE_SCHEMA = '%s' AND information_schema.TABLES.TABLE_NAME = '%s'" % (db_name, tb_name)
        rows = dbm.QueryAllSql(sql)
        if len(rows) == 1: # 数据表存在
            create_time_db = rows[0][0]
            modify_time_db = rows[0][1]
            if create_time_db != None:
                modify_time = create_time_db # 先赋创建时间
            if modify_time_db != None:
                modify_time = modify_time_db # 再赋更新时间
        return modify_time

    def GetDailyReport(self, account, date_s, date_e):
        save_path = ""
        dbm = self.dbm_clearx
        str_date_s = self.TransDateIntToStr(date_s)
        str_date_e = self.TransDateIntToStr(date_e)
        columns = ["trade_date", "account_id", "net_cumulative"]
        result = pd.DataFrame(columns = columns) # 空
        if dbm == None: # 直接读取本地文件
            if self.folder_clearx == "": # 缓存路径为空
                self.SendMessage("E", self.log_cate, "直接缓存获取 每日报表 时，本地数据缓存路径为空！")
            else:
                save_path = "%s/%s" % (self.folder_clearx, self.tb_daily_report)
                if not os.path.exists(save_path): # 缓存文件不存在
                    self.SendMessage("E", self.log_cate, "直接缓存获取 每日报表 时，本地数据缓存文件不存在！")
                else: # 读取缓存文件
                    result = pd.read_pickle(save_path)
        else: # 可以查询数据库
            need_query = False
            if self.folder_clearx == "": # 缓存路径为空
                need_query = True
            else:
                save_path = "%s/%s" % (self.folder_clearx, self.tb_daily_report)
                if not os.path.exists(save_path): # 缓存文件不存在
                    need_query = True
                else:
                    modify_time_lf = datetime.datetime.fromtimestamp(os.path.getmtime(save_path))
                    modify_time_db = self.GetTableModifyTime(dbm, self.db_clearx, self.tb_daily_report)
                    if modify_time_db != None and modify_time_lf < modify_time_db: # 数据库时间更新 # 如果 modify_time_db 为 None 估计数据库表不存在也就不用查询了
                        need_query = True
                    else: # 读取缓存文件
                        result = pd.read_pickle(save_path)
            if need_query == True: # 查询数据表
                sql = "SELECT trade_date, account_id, net_cumulative " + \
                      "FROM %s " % self.tb_daily_report + \
                      "WHERE account_id = '%s' AND trade_date >= '%s' AND trade_date <= '%s' " % (account, str_date_s, str_date_e) + \
                      "ORDER BY trade_date ASC, account_id ASC"
                rows = dbm.QueryAllSql(sql)
                if len(rows) > 0:
                    result = pd.DataFrame(data = list(rows), columns = columns)
                    if save_path != "": # 保存到文件
                        result.to_pickle(save_path)
        if result.empty:
            self.SendMessage("W", self.log_cate, "获取的 每日报表 为空！")
        return result

if __name__ == "__main__":
    folder = "../data" # 缓存文件夹
    valuex = ValueX()
    valuex.InitValueX(folder = folder) # 不使用数据库
    #valuex.InitValueX(host = "10.0.7.53", port = 3306, user = "user", passwd = "user", folder = folder)
    result = valuex.GetDailyReport("LHTZ_20170428001_000", 20170101, 20180228)
    if not result.empty:
        print(result)
