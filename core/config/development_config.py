'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/16 23:20
@Software: PyCharm
@File    : development_config.py
'''
"""
开发环境配置
"""
import os

from typing import Union, Optional

from pydantic import AnyHttpUrl, BaseSettings, IPvAnyAddress


class Settings(BaseSettings):
    # 开发模式配置
    DEBUG: bool = True
    # 项目文档
    TITLE: str = "FastAPI+MySQL"
    DESCRIPTION: str = "更多FastAPI知识，请关注我的个人网站 https://www.charmcode.cn/"
    # 文档地址 默认为docs
    DOCS_URL: str = "/api/docs"
    # 文档关联请求数据接口
    OPENAPI_URL: str = "/api/openapi.json"
    # redoc 文档
    REDOC_URL: Optional[str] = "/api/redoc"

    # token过期时间 分钟
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # 生成token的加密算法
    ALGORITHM: str = "HS256"

    # 生产环境保管好 SECRET_KEY
    SECRET_KEY: str = 'aeq)s(*&(&)()WEQasd8**&^9asda_asdasd*&*&^+_sda'

    # 项目根路径
    BASE_PATH: str = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))

    # 配置你的Mysql环境
    MYSQL_USERNAME: str = "fastapi"
    MYSQL_PASSWORD: str = "FastApi_test"
    MYSQL_HOST: str = "rm-uf6z20c639x3cwczwwo.mysql.rds.aliyuncs.com"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = 'fastapi'


    # MYSQL_USERNAME: str = "root"
    # MYSQL_PASSWORD: str = "zhouys618!"
    # MYSQL_HOST: str = "114.132.40.250"
    # MYSQL_PORT: int = 3306
    # MYSQL_DATABASE: str = 'blogs'
    # Mysql地址

    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@" \
                              f"{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4"

    # redis配置
    REDIS_HOST: str = "114.132.40.250"
    REDIS_PASSWORD: str = "zhouys618"
    REDIS_DB: int = 1
    REDIS_PORT: int = 6379
    REDIS_URL: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encoding=utf-8"
    REDIS_TIMEOUT: int = 5  # redis连接超时时间

    CASBIN_MODEL_PATH: str = "./common/model.conf"

    # 日志文件夹名
    LOGGER_FOLDER = "logs"
    # 日志文件名 (时间格式)
    LOGGER_NAME = '{time:YYYY-MM-DD_HH-mm-ss}.log'
    LOGGER_ENCODING = 'utf-8'
    LOGGER_LEVEL = 'DEBUG'  # ['DEBUG' | 'INFO']
    # 按 时间段 切分日志
    LOGGER_ROTATION = "100 MB"  # ["500 MB" | "12:00" | "1 week"]
    # 日志保留的时间, 超出将删除最早的日志
    LOGGER_RETENTION = "1 days"  # ["1 days"]

settings = Settings()