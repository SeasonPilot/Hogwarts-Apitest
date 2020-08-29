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
        .validate("json.headers.Accept", "application/json") \
        .validate("json.json.abc", 123)


# 参数共享
def test_httpbin_parameters_share():
    user_id = "adk129"
    ApiHttpbinGet() \
        .set_params(user_id=user_id) \
        .run() \
        .validate("status_code", 200) \
        .validate("headers.server", "gunicorn/19.9.0") \
        .validate("json().url", "http://www.httpbin.org/get?user_id={}".format(user_id)) \
        .validate("json().headers.Accept", "application/json")

    ApiHttpbinPost() \
        .set_json({"user_id": user_id}) \
        .run() \
        .validate("status_code", 200) \
        .validate("json.url", "http://www.httpbin.org/post") \
        .validate("json.headers.Accept", "application/json") \
        .validate("json.json.user_id", "adk129")


#  参数依赖、关联
# 实现提取状态码
def test_httpbin_extract():
    api_run = ApiHttpbinGet().run()
    status_code = api_run.extract("status_code")
    assert status_code == 200

    sever = api_run.extract("headers.server")
    assert sever == "gunicorn/19.9.0"

    accept_type = api_run.extract("json().headers.Accept")
    assert accept_type == "application/json"


def test_httpin_setcookies():
    api_run = ApiHttpbinGetCookies() \
        .set_cookie("freeform1", "123") \
        .set_cookie("freeform2", "456") \
        .run()
    freeform1 = api_run.extract("json.cookies.freeform1")
    freeform2 = api_run.extract("json.cookies.freeform2")
    assert freeform1 == "123"
    assert freeform2 == "456"


def test_httpbin_parameters_extract():
    # step 1:get value
    freeform = ApiHttpbinSetCookies() \
        .set_params(freeform=123) \
        .run() \
        .extract("json.cookies.freeform")
    assert freeform == "123"

    # step 2:use value as parameter
    ApiHttpbinPost() \
        .set_json({"freeform": freeform}) \
        .run() \
        .validate("status_code", 200) \
        .validate("json.url", "http://www.httpbin.org/post") \
        .validate("json.headers.Accept", "application/json") \
        .validate("json.json.freeform", freeform)


def test_httpbin_loggin_status(init_session):
    # step1: loggin and get cookie
    ApiHttpbinSetCookies().set_params(freeform=567).run(init_session)

    # step2: request another api, check cookie
    resp = ApiHttpbinPost() \
        .set_json({"abc": 123}) \
        .run(init_session) \
        .get_response()
    requests_headers = resp.request.headers

    assert "freeform=567" in requests_headers["Cookie"]
