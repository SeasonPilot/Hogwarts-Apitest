# _*_ coding:utf-8 _*_
# 作者：Season
# 时间：2020/8/26 21:39
# 文件名：test_core.py
# 开发工具：PyCharm
import requests
import pytest
from tests.api.httpbin import *


# 用例，单个接口以这样的方式进行描述，链式调用
def test_httpbin_get():
    ApiHttpbinGet().run() \
        .validate("status_code", 200) \
        .validate("headers.server", "gunicorn/19.9.0") \
        .validate("json().url", "http://www.httpbin.org/get") \
        .validate("json().args", {}) \
        .validate("json().headers.Accept", "application/json")


def test_httpbin_get_parmas():
    ApiHttpbinGet() \
        .set_params(adc=123, xyz=456) \
        .run() \
        .validate("status_code", 200) \
        .validate("headers.server", "gunicorn/19.9.0") \
        .validate("json().url", "http://www.httpbin.org/get?adc=123&xyz=456") \
        .validate("json().headers.Accept", "application/json")


def test_httpbin_post():
    ApiHttpbinPost() \
        .set_json({"abc": 123}) \
        .run() \
        .validate("status_code", 200) \
        .validate("json.url", "http://www.httpbin.org/post") \
        .validate("json.headers.Accept", "application/json")
