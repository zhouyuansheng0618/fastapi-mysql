# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：__init__.py.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/1 22:07
"""
"""

配置文件区分生产和开发

我这种是一种方式，简单直观
还有一种是服务一个固定路径放一个配置文件如 /etc/conf 下 xxx.ini 或者 xxx.py文件
然后项目默认读取 /etc/conf 目录下的配置文件，能读取则为生产环境，
读取不到则为开发环境，开发环境配置可以直接写在代码里面(或者配置ide环境变量)

根据环境变量ENV是否有值 区分生产开发
以上弃用

"""

import os

from .config import settings