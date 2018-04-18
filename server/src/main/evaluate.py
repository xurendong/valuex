
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

import math
import numpy as np
import pandas as pd

import config

class Evaluate():
    def __init__(self, **kwargs):
        self.daily_report = kwargs.get("daily_report", None) # 日期从早到晚排序
        self.config = config.config["config_p"]

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
        
        return average_daily_net_rise # 平均每日净值涨幅

    def CalcMaxMinPeriodReturn(self): # 002
        max_period_return = self.daily_report["daily_net_rise"].max()
        min_period_return = self.daily_report["daily_net_rise"].min()
        return max_period_return, min_period_return # 单周期最大涨幅、单周期最大跌幅

    def CalcGoUpProbability(self): # 003
        go_up_number = self.daily_report.ix[self.daily_report.daily_net_rise > 0.0, :].shape[0]
        go_up_probability = go_up_number / self.daily_report.shape[0]
        return go_up_probability # 上涨概率

    def CalcMaxDaysKeepUpOrDown(self): # 004
        days_keep_up = 0
        days_keep_down = 0
        max_days_keep_up = 0
        max_days_keep_down = 0
        loop_count= self.daily_report.shape[0] - 1
        for i in range(loop_count):
            if self.daily_report.iloc[i]["daily_net_rise"] > 0.0 and self.daily_report.iloc[i + 1]["daily_net_rise"] > 0.0:
                days_keep_up += 1
            if (self.daily_report.iloc[i]["daily_net_rise"] > 0.0 and self.daily_report.iloc[i + 1]["daily_net_rise"] <= 0.0) \
            or (i == loop_count and self.daily_report.iloc[i + 1]["daily_net_rise"] > 0.0): # 最后一个
                days_keep_up += 1
                if max_days_keep_up < days_keep_up:
                    max_days_keep_up = days_keep_up
                days_keep_up = 0
            
            if self.daily_report.iloc[i]["daily_net_rise"] < 0.0 and self.daily_report.iloc[i + 1]["daily_net_rise"] < 0.0:
                days_keep_down += 1
            if (self.daily_report.iloc[i]["daily_net_rise"] < 0.0 and self.daily_report.iloc[i + 1]["daily_net_rise"] >= 0.0) \
            or (i == loop_count and self.daily_report.iloc[i + 1]["daily_net_rise"] < 0.0): # 最后一个
                days_keep_down += 1
                if max_days_keep_down < days_keep_down:
                    max_days_keep_down = days_keep_down
                days_keep_down = 0
        return max_days_keep_up, max_days_keep_down

    # max_first_to_every：从起始日到每一天区间的最大值
    # every_day_drawdown：每天对应的最大回撤
    def CalcMaxDrawdown(self): # 005
        current_columns = self.daily_report.columns.tolist()
        current_columns.extend(["max_first_to_every", "every_day_drawdown"])
        self.daily_report = self.daily_report.reindex(columns = current_columns)
        
        self.daily_report["max_first_to_every"] = self.daily_report["net_cumulative"].expanding(min_periods = 1).max() # 从起始日到每一天区间的最大值
        self.daily_report["every_day_drawdown"] = self.daily_report["net_cumulative"] / self.daily_report["max_first_to_every"] - 1.0 # 每天对应的最大回撤
        
        daily_report_temp = self.daily_report.sort_values(by = ["every_day_drawdown"], ascending = True).reset_index(drop = True) # 按每日最大回撤从大到小排序（数值从小到大）
        # 目前只取第一个，暂不考虑有多个等值最大回撤的情况
        max_drawdown_date = daily_report_temp.iloc[0]["trade_date"]
        max_drawdown_value = daily_report_temp.iloc[0]["every_day_drawdown"]
        daily_report_temp = self.daily_report.ix[self.daily_report.trade_date <= max_drawdown_date, :] # 最大回撤发生日及之前
        daily_report_temp = daily_report_temp.sort_values(by = ["net_cumulative"], ascending = False).reset_index(drop = True) # 按累计净值从大到小排序
        drawdown_start_date = daily_report_temp.iloc[0]["trade_date"]
        
        #print_matrix = self.daily_report.loc[:, ["trade_date", "max_first_to_every", "every_day_drawdown"]]
        #print(print_matrix)
        
        return max_drawdown_value, max_drawdown_date, drawdown_start_date # 最大回撤、最大回撤日期、回撤开始日期

    def CalcAnnualReturnRate(self): # 006
        period_days = pd.period_range(self.daily_report["trade_date"].iloc[0], self.daily_report["trade_date"].iloc[-1], freq = "D") # 自然日填充
        annual_return_rate = pow(self.daily_report.ix[self.daily_report.shape[0] - 1, "net_cumulative"] / self.daily_report.ix[0, "net_cumulative"], self.config.days_of_year / len(period_days)) - 1.0
        index_annual_return_rate = pow(self.daily_report.ix[self.daily_report.shape[0] - 1, "refer_index"] / self.daily_report.ix[0, "refer_index"], self.config.days_of_year / len(period_days)) - 1.0
        return annual_return_rate, index_annual_return_rate # 年化收益率、参照指数年化收益率

    def CalcReturnVolatility(self): # 007
        return_volatility = self.daily_report["daily_net_rise"].std() * math.sqrt(self.config.days_of_year)
        return return_volatility # 收益波动率

    def CalcSharpeRatio(self, annual_return_rate, return_volatility): # 008
        sharpe_ratio = (annual_return_rate - self.config.benchmark_rate) / return_volatility
        return sharpe_ratio # 夏普比率

    # pre_refer_index     ：上日参照指数
    # daily_index_increase：每日参照指数增长
    # daily_index_rise    ：每日参照指数涨幅
    def CalcBetaValue(self): # 009
        current_columns = self.daily_report.columns.tolist()
        current_columns.extend(["pre_refer_index", "daily_index_increase", "daily_index_rise"])
        self.daily_report = self.daily_report.reindex(columns = current_columns)
        
        self.daily_report["pre_refer_index"] = self.daily_report["refer_index"].shift(1)
        self.daily_report["daily_index_increase"] = self.daily_report["refer_index"].diff(1)
        self.daily_report["daily_index_rise"] = self.daily_report["daily_index_increase"] / self.daily_report["pre_refer_index"]
        
        #print_matrix = self.daily_report.loc[:, ["trade_date", "refer_index", "pre_refer_index", "daily_index_increase", "daily_index_rise"]]
        #print(print_matrix)
        
        beta_value = self.daily_report["daily_net_rise"].cov(self.daily_report["daily_index_rise"]) / self.daily_report["daily_index_rise"].var()
        return beta_value # 贝塔值

    def CalcAlphaValue(self, annual_return_rate, index_annual_return_rate, beta_value): # 010
        alpha_value = (annual_return_rate - self.config.benchmark_rate) - beta_value * (index_annual_return_rate - self.config.benchmark_rate)
        return alpha_value # 阿尔法值
