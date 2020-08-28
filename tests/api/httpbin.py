# _*_ coding:utf-8 _*_
# 作者：Season
# 时间：2020/8/28 21:42
# 文件名：httpbin.py
# 开发工具：PyCharm
from hogwarts_apitest.api import BaseApi


# 接口以类这种方式定义
class ApiHttpbinGet(BaseApi):
    url = "http://www.httpbin.org/get"
    method = "GET"
    headers = {"accept": "application/json"}


class ApiHttpbinPost(BaseApi):
    url = "http://www.httpbin.org/post"
    method = "POST"
    params = {}
    headers = {"accept": "application/json"}
    # data 优先级高于json
    json = {"abc": 123}


class ApiHttpbinGetCookies(BaseApi):
    url = "http://www.httpbin.org/cookies"
    method = "GET"
    params = {}
    headers = {"accept": "application/json"}
