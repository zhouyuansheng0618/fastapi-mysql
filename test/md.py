# encoding: utf-8
"""
@author: zhouys
@contact: zhouys618@163.com
@software: PyCharm
@file: md.py
@time: 2021/12/16 22:21
"""
# md5加密

from jose import jwt
from passlib.context import CryptContext

from common.security import create_access_token
from core.config.development_config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password: str, hashed_password: str,salt:str) -> bool:
    """
    验证密码
    :param plain_password: 原密码
    :param hashed_password: hash后的密码
    :return:
    """
    return pwd_context.verify(plain_password+salt, hashed_password)

# if __name__ == '__main__':

#     verify_password('admin',)