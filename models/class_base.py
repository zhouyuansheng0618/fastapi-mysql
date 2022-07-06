# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：class_base.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/2 15:58
"""
from typing import Any
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime,String

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from nanoid import generate

@as_declarative()
class Base:
    # 通用的字段
    id = Column(String(10),primary_key=True, default=generate(size=10), comment="id")
    create_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    is_delete = Column(Integer, default=0, comment="逻辑删除:0=未删除,1=删除")
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        import re
        # 如果没有指定__tablename__  则默认使用model类名转换表名字
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        # 表明格式替换成_格式 如 MallUser 替换成 mall_user
        return "_".join(name_list).lower()