'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/17 22:49
@Software: PyCharm
@File    : response_code.py
'''
from pydantic.generics import GenericModel

from common.logger import logger

"""

统一响应状态码

"""
from typing import Union, TypeVar, Generic, Type

from fastapi import status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi import status as http_status

def resp_200(*, data: Union[list, dict, str] = None, message: str = "Success") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 200,
            'message': message,
            'data': data,
        })
    )


def resp_500(*, data: Union[list, dict, str] = None,
             message: str = "Internal Server Error") -> Response:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({
            'code': 500,
            'message': message,
            'data': data,
        })
    )


# 请求参数格式错误
def resp_4001(*, data: Union[list, dict, str] = None,
              message: Union[list, dict, str] = "Request Validation Error") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 4001,
            'data': data,
            'message': message,
        })
    )


# 用户token过期
def resp_4002(*, data: Union[list, dict, str] = None, message: str = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 4002,
            'data': data,
            'message': message,
        })
    )


# 找不到该数据
def resp_4003(*, data: Union[list, dict, str] = None, message: str = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 4002,
            'data': data,
            'message': message,
        })
    )


# token认证失败
def resp_4003(*, data: Union[list, dict, str] = None, message: str = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 4003,
            'data': data,
            'message': message,
        })
    )


# 内部验证数据错误
def resp_5002(*, data: Union[list, dict, str] = None,
              message: Union[list, dict, str] = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 5002,
            'data': data,
            'message': message,
        })
    )


SchemasType = TypeVar("SchemasType")


class RestfulModel(GenericModel, Generic[SchemasType]):
    code: int
    data: SchemasType = None
    msg: str


def response(code: int = 200, data: Type[SchemasType] = None, msg: str = 'Success'):
    if code == 200:
        logger.info(msg)
    elif code == 404:
        logger.error(msg)
    else:
        logger.warning(msg)
    return {'code': code, 'data': data, 'msg': msg}
class Resp(object):
    def __init__(self, status: int, msg: str, code: int):
        self.status = status
        self.msg = msg
        self.code = code

    def set_msg(self, msg):
        self.msg = msg
        return self


InvalidRequest: Resp = Resp(1000, "无效的请求", http_status.HTTP_400_BAD_REQUEST)
InvalidParams: Resp = Resp(1002, "无效的参数", http_status.HTTP_400_BAD_REQUEST)
BusinessError: Resp = Resp(1003, "业务错误", http_status.HTTP_400_BAD_REQUEST)
DataNotFound: Resp = Resp(1004, "查询失败", http_status.HTTP_400_BAD_REQUEST)
DataStoreFail: Resp = Resp(1005, "新增失败", http_status.HTTP_400_BAD_REQUEST)
DataUpdateFail: Resp = Resp(1006, "更新失败", http_status.HTTP_400_BAD_REQUEST)
DataDestroyFail: Resp = Resp(1007, "删除失败", http_status.HTTP_400_BAD_REQUEST)
PermissionDenied: Resp = Resp(1008, "权限拒绝", http_status.HTTP_403_FORBIDDEN)
ServerError: Resp = Resp(5000, "服务器繁忙", http_status.HTTP_500_INTERNAL_SERVER_ERROR)


def ok(*, data: Union[list, dict, str] = None, pagination: dict = None, msg: str = "success") -> Response:
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content=jsonable_encoder({
            'status': 200,
            'msg': msg,
            'data': data,
            'pagination': pagination
        })
    )


def fail(resp: Resp) -> Response:
    return JSONResponse(
        status_code=resp.code,
        content=jsonable_encoder({
            'status': resp.status,
            'msg': resp.msg,
        })
    )