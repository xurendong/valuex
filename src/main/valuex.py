
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

import assess

if __name__ == "__main__":
    data_folder = "../data" # 数据文件夹
    temp_folder = "../temp" # 模板文件夹
    rets_folder = "../rets" # 结果文件夹
    instance = assess.Assess()
    instance.InitAssess(data_folder = data_folder, temp_folder = temp_folder, rets_folder = rets_folder) # 不使用数据库
    #instance.InitAssess(host = "10.0.7.53", port = 3306, user = "user", passwd = "user", data_folder = data_folder, temp_folder = temp_folder, rets_folder = rets_folder)
    result = instance.GetDailyReport("LHTZ_20170428001_000", 20170101, 20180228)
    if not result.empty:
        print(result)
    instance.ExportResultReport()
