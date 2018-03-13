
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

import codecs

import jinja2
import pdfkit

try: import logger
except: pass

pdfkit_options = {
    "page-size": "A4", # Letter
    "minimum-font-size": 10, 
    "image-dpi": 300, 
    "margin-top": "0.75in", 
    "margin-right": "0.75in", 
    "margin-bottom": "0.75in", 
    "margin-left": "0.75in", 
    "encoding": "UTF-8", # 支持中文
    "custom-header": [
        ("Accept-Encoding", "gzip"), 
    ], 
    "cookie": [
        ("cookie-name-1", "cookie-value-1"), 
        ("cookie-name-2", "cookie-value-2"), 
    ], 
    "outline-depth": 4, # "no-outline": None, 
    "quiet": "", 
}

class Report():
    def __init__(self, **kwargs):
        self.log_text = ""
        self.log_cate = "Report"
        self.log_show = "V"
        self.log_inst = None
        try: self.log_inst = logger.Logger()
        except: pass
        self.temp_folder = kwargs.get("temp_folder", "")
        self.rets_folder = kwargs.get("rets_folder", "")
        self.temp_file_report = "report.html"
        self.rets_file_pdf = self.rets_folder + "/report.pdf"
        self.rets_file_html = self.rets_folder + "/report.html"

    def __del__(self):
        pass

    def SendMessage(self, log_type, log_cate, log_info):
        if self.log_inst != None:
            self.log_inst.SendMessage(log_type, log_cate, log_info, self.log_show)
        else:
            print("%s：%s：%s" % (log_type, log_cate, log_info))

    def CreateReport(self, template):
        try:
            report = template.render(name = "Hello World 你好世界") # TODO:
            return report
        except jinja2.TemplateNotFound as e:
            self.log_text = "Create 模板 %s 不存在：%s！" % (e.name, e.message)
            self.SendMessage("E", self.log_cate, self.log_text)
        except jinja2.TemplateSyntaxError as e:
            self.log_text = "Create 模板 %s 语法错误：%s %d %s！" % (e.name, e.filename, e.lineno, e.message)
            self.SendMessage("E", self.log_cate, self.log_text)
        except jinja2.TemplateRuntimeError as e:
            self.log_text = "Create 模板运行时错误：%s！" % e.message
            self.SendMessage("E", self.log_cate, self.log_text)
        except jinja2.UndefinedError as e:
            self.log_text = "Create 模板未定义错误：%s！" % e.message
            self.SendMessage("E", self.log_cate, self.log_text)
        except jinja2.TemplateError as e:
            self.log_text = "Create 模板错误：%s！" % e.message
            self.SendMessage("E", self.log_cate, self.log_text)
        except:
            self.SendMessage("E", self.log_cate, "Create 未知错误！")
        return ""

    def ExportReport(self):
        try:
            environment = jinja2.Environment(loader = jinja2.FileSystemLoader(self.temp_folder, "utf-8"), autoescape = jinja2.select_autoescape(["html", "xml"]))
            template_report = environment.get_template(self.temp_file_report)
            with codecs.open(self.rets_file_html, "w", "utf-8") as fd: # 必需指定编码，不然生成的 PDF 中文乱码
                report = self.CreateReport(template_report)
                if report != "":
                    fd.write(report)
                    fd.close()
                else:
                    self.SendMessage("E", self.log_cate, "创建报告内容失败！")
                    fd.close()
                    return False
            #pdfkit_config = pdfkit.configuration(wkhtmltopdf = "D:/PdfKit/bin/wkhtmltopdf.exe") # 或者环境变量 path 添加 D:\PdfKit\bin
            #pdfkit.from_file(["./result_1.html", "./result_2.html"], "report.pdf", options = pdfkit_options) # 可以用列表整合多个文件
            #pdfkit.from_url(["http://livesino.net/", "https://cn.engadget.com/"], "report.pdf") # 使用 options 的话可能因为 UTF-8 而乱码
            #pdfkit.from_string(template_report.render(name = "Hello World"), "report.pdf", options = pdfkit_options, configuration = pdfkit_config)
            pdfkit.from_file(self.rets_file_html, self.rets_file_pdf, options = pdfkit_options)
            return True
        except jinja2.TemplateNotFound as e:
            self.log_text = "Export 模板 %s 不存在：%s！" % (e.name, e.message)
            self.SendMessage("E", self.log_cate, self.log_text)
        except jinja2.TemplateSyntaxError as e:
            self.log_text = "Export 模板 %s 语法错误：%s %d %s！" % (e.name, e.filename, e.lineno, e.message)
            self.SendMessage("E", self.log_cate, self.log_text)
        except jinja2.TemplateRuntimeError as e:
            self.log_text = "Export 模板运行时错误：%s！" % e.message
            self.SendMessage("E", self.log_cate, self.log_text)
        except jinja2.UndefinedError as e:
            self.log_text = "Export 模板未定义错误：%s！" % e.message
            self.SendMessage("E", self.log_cate, self.log_text)
        except jinja2.TemplateError as e:
            self.log_text = "Export 模板错误：%s！" % e.message
            self.SendMessage("E", self.log_cate, self.log_text)
        except:
            self.SendMessage("E", self.log_cate, "Export 未知错误！")
        return False
