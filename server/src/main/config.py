
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

class BasicConfig: # 基本
    days_of_year = 250
    benchmark_rate = 0.031036 # 无风险利率 = 起始日十年期国债收益率
    items_per_page = 10

class Config_P(BasicConfig): # 生产
    produce = True

class Config_D(BasicConfig): # 开发
    develop = True

class Config_T(BasicConfig): # 测试
    testing = True

config = {"config_p" : Config_P, "config_d" : Config_D, "config_t" : Config_T}
