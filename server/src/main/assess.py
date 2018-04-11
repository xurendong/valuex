
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
import re
import datetime

import xlrd
import numpy as np
import pandas as pd

try: import logger
except: pass
import common
import dbm_mysql
import report

class DailyReportItem(object):
    def __init__(self, **kwargs):
        self.trade_date = kwargs.get("trade_date", datetime.datetime(1970, 1, 1))
        self.account_id = kwargs.get("account_id", "")
        self.net_unit = kwargs.get("net_unit", 0.0)
        self.net_cumulative = kwargs.get("net_cumulative", 0.0)

    def ToString(self):
        return "trade_date：%s, " % self.trade_date.strftime("%Y-%m-%d") + \
               "account_id：%s, " % self.account_id + \
               "net_unit：%f, " % self.net_unit + \
               "net_cumulative：%f" % self.net_cumulative

class Assess(common.Singleton):
    def __init__(self):
        self.log_text = ""
        self.log_cate = "Assess"
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

    def InitAssess(self, **kwargs):
        self.host = kwargs.get("host", "0.0.0.0")
        self.port = kwargs.get("port", 0)
        self.user = kwargs.get("user", "user")
        self.passwd = kwargs.get("passwd", "123456")
        self.charset = "utf8"
        self.data_folder = kwargs.get("data_folder", "") # 数据文件夹
        self.temp_folder = kwargs.get("temp_folder", "") # 模板文件夹
        self.rets_folder = kwargs.get("rets_folder", "") # 结果文件夹
        self.db_clearx = "clearx"
        self.tb_daily_report = "daily_report"
        
        self.flag_use_database = True
        if self.host == "0.0.0.0": # 不使用数据库
            self.flag_use_database = False
        
        self.folder_clearx = ""
        if self.data_folder != "":
            self.folder_clearx = self.data_folder + "/clearx"
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

    def SaveUploadData(self, data_file):
        sheet_name = "daily_report"
        daily_report_list = []
        xls_file = xlrd.open_workbook(data_file)
        try:
            xls_sheet = xls_file.sheet_by_name(sheet_name)
        except:
            self.log_text = "上传文件 %s 表单异常！%s" % (data_file, sheet_name)
            self.SendMessage("E", self.log_cate, self.log_text)
            return False
        xls_rows = xls_sheet.nrows
        xls_cols = xls_sheet.ncols
        if xls_rows < 2:
            self.log_text = "上传文件 %s 行数异常！%d" % (data_file, xls_rows)
            self.SendMessage("E", self.log_cate, self.log_text)
            return False
        if xls_cols < 4:
            self.log_text = "上传文件 %s 列数异常！%d" % (data_file, xls_cols)
            self.SendMessage("E", self.log_cate, self.log_text)
            return False
        for i in range(xls_rows):
            if i > 0:
                trade_date = common.TransDateIntToDate(xls_sheet.row(i)[0].value)
                account_id = xls_sheet.row(i)[1].value
                net_unit = xls_sheet.row(i)[2].value
                net_cumulative = xls_sheet.row(i)[3].value
                daily_report_item = DailyReportItem(trade_date = trade_date, account_id = account_id, net_unit = net_unit, net_cumulative = net_cumulative)
                daily_report_list.append(daily_report_item)
        #for item in daily_report_list:
        #    print(item.ToString())
        self.log_text = "上传文件导入每日报表数据 %d 行。%s" % (len(daily_report_list), data_file)
        if len(daily_report_list) <= 0:
            self.SendMessage("W", self.log_cate, self.log_text)
            return False
        else:
            self.SendMessage("I", self.log_cate, self.log_text)
        
        # 先存数据库，后存本地文件，这样 GetDailyReport() 时数据库修改时间就不会晚于本地文件
        
        dbm = self.dbm_clearx
        if dbm != None: # 需要保存至数据库
            sql = "SHOW TABLES"
            data_tables = [dbm.QueryAllSql(sql)]
            #print data_tables
            have_tables = re.findall("(\'.*?\')", str(data_tables))
            have_tables = [re.sub("'", "", table) for table in have_tables]
            #print have_tables
            if self.tb_daily_report in have_tables:
                sql = "TRUNCATE TABLE %s" % self.tb_daily_report
                dbm.ExecuteSql(sql)
            else:
                sql = "CREATE TABLE `%s` (" % self.tb_daily_report + \
                      "`id` int(32) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增序号'," + \
                      "`trade_date` date NOT NULL COMMENT '交易日期'," + \
                      "`account_id` varchar(32) NOT NULL COMMENT '账户编号'," + \
                      "`net_unit double(16,4) DEFAULT '0.00' COMMENT '单位净值'," + \
                      "`net_cumulative` double(16,4) DEFAULT '0.00' COMMENT '累计净值'," + \
                      "PRIMARY KEY (`id`)," + \
                      "UNIQUE KEY `idx_trade_date_account_id` (`trade_date`,`account_id`)" + \
                      ") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8"
                dbm.ExecuteSql(sql)
            values_list = []
            save_index_from = 0 #
            save_record_failed = 0
            save_record_success = 0
            total_record_number = len(daily_report_list)
            sql = "INSERT INTO %s" % self.tb_daily_report + "(trade_date, account_id, net_unit, net_cumulative) VALUES (%s, %s, %s, %s)"
            for i in range(save_index_from, total_record_number):
                str_trade_date = daily_report_list[i].trade_date.strftime("%Y-%m-%d")
                values_list.append((str_trade_date, daily_report_list[i].account_id, daily_report_list[i].net_unit, daily_report_list[i].net_cumulative))
                if (i - save_index_from + 1) % 3000 == 0: # 自定义每批次保存条数
                    if len(values_list) > 0: # 有记录需要保存
                        if dbm.ExecuteManySql(sql, values_list) == False:
                            save_record_failed += len(values_list)
                        else:
                            save_record_success += len(values_list)
                        #print("保存：", len(values_list))
                        values_list = [] #
            if len(values_list) > 0: # 有记录需要保存
                if dbm.ExecuteManySql(sql, values_list) == False:
                    save_record_failed += len(values_list)
                else:
                    save_record_success += len(values_list)
                #print("保存：", len(values_list))
            self.log_text = "每日报表数据入库：总共 %d 条，成功 %d 条，失败 %d 条。" % (total_record_number, save_record_success, save_record_failed)
            self.SendMessage("I", self.log_cate, self.log_text)
        
        if len(daily_report_list) > 0: # 上面已检查
            columns = ["trade_date", "account_id", "net_unit", "net_cumulative"]
            result = pd.DataFrame(columns = columns) # 空
            if self.folder_clearx == "": # 缓存路径为空
                self.SendMessage("E", self.log_cate, "缓存数据 每日报表 时，本地数据缓存路径为空！")
            else:
                result = pd.DataFrame(data = [[item.trade_date, item.account_id, item.net_unit, item.net_cumulative] for item in daily_report_list], columns = columns)
                save_path = "%s/%s" % (self.folder_clearx, self.tb_daily_report)
                result.to_pickle(save_path)
            #if not result.empty:
            #    print(result)
            self.log_text = "每日报表数据缓存：总共 %d 条，成功 %d 条。%s" % (len(daily_report_list), result.shape[0], save_path)
            self.SendMessage("I", self.log_cate, self.log_text)
        
        return True

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
        str_date_s = common.TransDateIntToStr(date_s)
        str_date_e = common.TransDateIntToStr(date_e)
        date_date_s = common.TransDateIntToDate(date_s)
        date_date_e = common.TransDateIntToDate(date_e)
        columns = ["trade_date", "account_id", "net_unit", "net_cumulative"]
        result = pd.DataFrame(columns = columns) # 空
        locals = pd.DataFrame(columns = columns) # 空
        if dbm == None: # 直接读取本地文件
            if self.folder_clearx == "": # 缓存路径为空
                self.SendMessage("E", self.log_cate, "直接缓存获取 每日报表 时，本地数据缓存路径为空！")
            else:
                save_path = "%s/%s" % (self.folder_clearx, self.tb_daily_report)
                if not os.path.exists(save_path): # 缓存文件不存在
                    self.SendMessage("E", self.log_cate, "直接缓存获取 每日报表 时，本地数据缓存文件不存在！")
                else: # 读取缓存文件
                    locals = pd.read_pickle(save_path)
                    self.SendMessage("I", self.log_cate, "本地缓存 获取 %d 条 每日报表 数据。" % locals.shape[0])
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
                        locals = pd.read_pickle(save_path)
                        self.SendMessage("I", self.log_cate, "本地缓存 获取 %d 条 每日报表 数据。" % locals.shape[0])
            if need_query == True: # 查询数据表
                sql = "SELECT trade_date, account_id, net_unit, net_cumulative " + \
                      "FROM %s " % self.tb_daily_report + \
                      "WHERE account_id = '%s' AND trade_date >= '%s' AND trade_date <= '%s' " % (account, str_date_s, str_date_e) + \
                      "ORDER BY trade_date ASC, account_id ASC"
                rows = dbm.QueryAllSql(sql)
                if len(rows) > 0:
                    result = pd.DataFrame(data = list(rows), columns = columns)
                    if save_path != "": # 保存到文件
                        result.to_pickle(save_path)
                self.SendMessage("I", self.log_cate, "数据库 获取 %d 条 每日报表 数据。" % result.shape[0])
            else: # 过滤数据
                locals = locals.ix[(locals.account_id == account), :] # 如果上传的数据只是单账户的则可以省略这步
                result = locals.ix[(locals.trade_date >= date_date_s) & (locals.trade_date <= date_date_e), :]
                self.SendMessage("I", self.log_cate, "本地缓存 滤得 %d 条 每日报表 数据。" % result.shape[0])
        if result.empty:
            self.SendMessage("W", self.log_cate, "获取的 每日报表 为空！")
        return result

    def StrategyEvaluation(self, daily_report):
        # TODO:
        return True

    def ExportResultReport(self):
        self.report = report.Report(temp_folder = self.temp_folder, rets_folder = self.rets_folder)
        ret = self.report.ExportReport()
        if ret == True:
            self.SendMessage("I", self.log_cate, "导出报告成功。")
        else:
            self.SendMessage("I", self.log_cate, "导出报告失败！")
        return ret
