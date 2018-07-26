
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

import logging
from logging.handlers import TimedRotatingFileHandler

import common

logger = logging.getLogger("ValueX")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(levelname)-5s %(message)s")

debuger = TimedRotatingFileHandler("..\logs\ValueX_%s.log" % common.GetDateShort(), "D", 1)
debuger.setLevel(logging.DEBUG)
debuger.setFormatter(formatter)
logger.addHandler(debuger)

errorer = TimedRotatingFileHandler("..\logs\ValueX_%s_E.log" % common.GetDateShort(), "D", 1)
errorer.setLevel(logging.ERROR)
errorer.setFormatter(formatter)
logger.addHandler(errorer)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)

class Logger(common.Singleton):
    def __init__(self):
        self.log_inst = logger

    def __del__(self):
        pass

    def SendMessage(self, log_type, log_cate, log_info, log_show = ""):
        if log_type == "D" or log_type == "I" or log_type == "H" or log_type == "W":
            self.log_inst.debug("%s <%s> - %s" % (log_type, log_cate, log_info))
        elif log_type == "E" or log_type == "F":
            self.log_inst.error("%s <%s> - %s" % (log_type, log_cate, log_info))
        if log_show != "":
            print("%s %s %s <%s> - %s" % (common.GetDateShort(), common.GetTimeShort(), log_type, log_cate, log_info))
