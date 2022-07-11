'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/17 22:42
@Software: PyCharm
@File    : logger.py
'''
# import os
# import time
# from loguru import logger
# from core.config.development_config import settings
#
# # 定位到log日志文件
# log_path = os.path.join(settings.BASE_PATH, 'logs')
#
# if not os.path.exists(log_path):
#     os.mkdir(log_path)
#
# log_path_error = os.path.join(log_path,
#                               f'{time.strftime("%Y-%m-%d")}_error.log')
# log_path_info = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_info.log')
# log_path_warning = os.path.join(log_path,
#                                 f'{time.strftime("%Y-%m-%d")}_warning.log')
# # 日志简单配置
# # logger.add(log_path_error, rotation="12:00", retention="5 days", enqueue=True)
# # 日志简单配置 文件区分不同级别的日志
# logger.add(log_path_info,
#            rotation="50 MB",
#            encoding='utf-8',
#            enqueue=True,
#            level='INFO',
#            compression='zip',
#            retention=5)
#
# logger.add(log_path_warning,
#            rotation="50 MB",
#            encoding='utf-8',
#            enqueue=True,
#            level='WARNING',
#            compression='zip',
#            retention=5)
#
# logger.add(log_path_error,
#            rotation="50 MB",
#            encoding='utf-8',
#            enqueue=True,
#            level='ERROR',
#            compression='zip',
#            retention=5)
#
# __all__ = ["logger"]
import os

from loguru import logger

from core.config.development_config import settings


def logs_path():
    # 获取当前文件夹
    current_path = os.path.dirname(__file__)

    # 获取当前文件夹的上一层文件
    base_path = os.path.abspath(os.path.join(current_path, ".."))

    # 拼接日志的路径
    log_path = base_path + os.sep + settings.LOGGER_FOLDER + os.sep
    # print(f'日志文件夹名: {log_path} \n')

    """如果文件夹不存在就创建"""
    os.makedirs(log_path, exist_ok=True)

    return log_path


""" 保留日志文件夹下最大个数(自己调试用) """
file_list = os.listdir(logs_path())
if len(file_list) > 4:
    os.remove(os.path.join(logs_path(), file_list[0]))

# 日志输出路径
log_path_name = os.path.join(logs_path(), settings.LOGGER_NAME)

# 详见: https://loguru.readthedocs.io/en/stable/overview.html#features
logger.add(log_path_name,
           encoding=settings.LOGGER_ENCODING,
           level=settings.LOGGER_LEVEL,
           rotation=settings.LOGGER_ROTATION,
           retention=settings.LOGGER_RETENTION,
           enqueue=True)

if __name__ == '__main__':
    logger.warning("warning")
    logger.info("info")
    logger.error("error")
    logger.critical("critical")
    logger.debug("debug")