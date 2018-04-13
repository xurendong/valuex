
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

import numpy as np
import pandas as pd

class Evaluate():
    def __init__(self, **kwargs):
        self.daily_report = kwargs.get("daily_report", None) # 日期从早到晚排序

    def __del__(self):
        pass

    # pre_net_unit      ：上日单位净值
    # pre_net_cumulative：上日累计净值
    # daily_net_increase：每日净值增长
    # daily_net_rise    ：每日净值涨幅
    def CalcAverageDailyNetRise(self): # 001
        current_columns = self.daily_report.columns.tolist()
        current_columns.extend(["pre_net_unit", "pre_net_cumulative", "daily_net_increase", "daily_net_rise"])
        self.daily_report = self.daily_report.reindex(columns = current_columns)
        
        self.daily_report["pre_net_unit"] = self.daily_report["net_unit"].shift(1)
        self.daily_report["pre_net_cumulative"] = self.daily_report["net_cumulative"].shift(1)
        self.daily_report["daily_net_increase"] = self.daily_report["net_cumulative"].diff(1)
        self.daily_report["daily_net_rise"] = self.daily_report["daily_net_increase"] / self.daily_report["pre_net_cumulative"]
        
        average_daily_net_rise = self.daily_report["daily_net_rise"].mean(axis = 0, skipna = True)
        
        #print_matrix = self.daily_report.loc[:, ["trade_date", "pre_net_unit", "pre_net_cumulative", "daily_net_increase", "daily_net_rise"]]
        #print(print_matrix)
        
        return average_daily_net_rise

    def CalcAnnualReturnRate(self): # 002
        period_days = pd.period_range(self.daily_report["trade_date"].iloc[0], self.daily_report["trade_date"].iloc[-1], freq = "D")
        annual_return_rate = pow(self.daily_report.ix[self.daily_report.shape[0] - 1, "net_cumulative"] / self.daily_report.ix[0, "net_cumulative"], 250.0 / len(period_days)) - 1.0
        return annual_return_rate
