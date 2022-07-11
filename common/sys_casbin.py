'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/21 16:17
@Software: PyCharm
@File    : sys_casbin.py
'''
import casbin
# from casbin import util
import casbin_sqlalchemy_adapter

from db.session import engine
from core.config.development_config import settings


def get_casbin() -> casbin.Enforcer:
    adapter = casbin_sqlalchemy_adapter.Adapter(engine)

    e = casbin.Enforcer(settings.CASBIN_MODEL_PATH, adapter)

    return e
