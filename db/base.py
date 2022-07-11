'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/16 22:59
@Software: PyCharm
@File    : base.py
'''
# 需要使用 alembic 生成表的 记得在这里 从models里面 倒入进来才行 否则不会生成
# imported by Alembic # 方便在Alembic导入,迁移用
from db.base_class import Base
# from models.blog import BlogTag, Category, CityVisitor, Comment, Blog, Friend
# from models.log import ExceptionLog, LoginLog, OperationLog, ScheduleJobLog, VisitLog
# from models.settings import About, VisitRecord, SiteSetting, Tag, Visitor, ScheduleJob, Moment
from models.user import User, Permission, Role, UserGroup, Account, UserRole, UserGroupRole, UserGroupUser, \
    RolePermission
