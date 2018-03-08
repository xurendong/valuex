
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

import logging
from datetime import datetime

from logging.handlers import TimedRotatingFileHandler

import common

logger = logging.getLogger("ValueX")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(levelname)-5s %(message)s")

debuger = TimedRotatingFileHandler("..\logs\ValueX_%s.log" % datetime.now().strftime("%Y-%m-%d"), "D", 1)
debuger.setLevel(logging.DEBUG)
debuger.setFormatter(formatter)
logger.addHandler(debuger)

errorer = TimedRotatingFileHandler("..\logs\ValueX_%s_E.log" % datetime.now().strftime("%Y-%m-%d"), "D", 1)
errorer.setLevel(logging.ERROR)
errorer.setFormatter(formatter)
logger.addHandler(errorer)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)

class Logger(common.Singleton):
    def __init__(self):
        self.logInst = logger

    def __del__(self):
        pass

    def SendMessage(self, logType, logCate, logInfo, logShow = ""):
        if logType == "D" or logType == "I" or logType == "H" or logType == "W":
            self.logInst.debug(logInfo)
        elif logType == "E" or logType == "F":
            self.logInst.error(logInfo)
