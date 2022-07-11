# -*- coding: utf-8 -*- 
# @Time : 2022/7/8 13:43 
# @Author : zhouys618@163.com 
# @File : user.py 
# @desc:
from datetime import datetime
from pydantic import Field, BaseModel, validator
from typing import Optional, List
from schemas.base import BaseResp, ResAntTable


class BaseUser(BaseModel):
    pass


class CreateUser(BaseUser):
    pass


class UpdateUser(BaseUser):
    pass


class DeleteUser(BaseUser):
    pass


class QueryUser(BaseUser):
    pass
