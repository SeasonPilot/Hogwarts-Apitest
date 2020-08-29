# _*_ coding:utf-8 _*_
# 作者：Season
# 时间：2020/8/29 16:27
# 文件名：conftest.py
# 开发工具：PyCharm
import pytest
import requests


@pytest.fixture(scope="function")
def init_session():
    return requests.sessions.Session()
