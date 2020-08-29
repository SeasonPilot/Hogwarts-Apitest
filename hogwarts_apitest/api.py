# _*_ coding:utf-8 _*_
# 作者：Season
# 时间：2020/8/27 23:23
# 文件名：api.py
# 开发工具：PyCharm
import requests


class BaseApi(object):
    session = requests.sessions.Session()
    url = ""
    method = "GET"
    headers = {}
    cookies = {}
    params = {}
    data = {}
    json = {}

    def set_data(self, data):
        self.data = data
        return self

    def set_json(self, json_data):
        self.json = json_data
        return self

    def set_params(self, **params):
        self.params = params
        return self

    def set_cookie(self, key, value):
        self.cookies.update({key: value})
        return self

    def run(self):
        self.response = self.session.request(
            self.method,
            self.url,
            params=self.params,
            cookies=self.cookies,
            headers=self.headers,
            data=self.data,
            json=self.json
        )
        return self

    def validate(self, key, expected_value):
        actual_value = self.extract(key)
        assert actual_value == expected_value
        return self

    def extract(self, field):
        value = self.response
        for _key in field.split("."):
            print("value---------------", _key, value)
            if isinstance(value, requests.Response):
                if _key in ["json()", "json"]:
                    value = self.response.json()
                else:
                    value = getattr(value, _key)
            elif isinstance(value, (requests.structures.CaseInsensitiveDict, dict)):
                value = value[_key]
        return value

    def get_response(self):
        return self.response
