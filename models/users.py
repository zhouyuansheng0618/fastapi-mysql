# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：users.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/1 22:19
"""
# from class_base import Base
from models.class_base import Base
from sqlalchemy import Boolean, Column, Integer, String, VARCHAR, BIGINT
class User(Base):
    __tablename__ = "user"
    # id = Column(Integer,  autoincrement=True)
    email = Column(String(128), unique=True, index=True, nullable=False, comment="邮箱")
