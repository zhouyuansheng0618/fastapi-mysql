# encoding: utf-8
"""
@author: zhouys
@contact: zhouys618@163.com
@software: PyCharm
@file: base.py
@time: 2021/12/13 22:43
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD对象的默认方法去 增 查 改 删 (CRUD).

        参数 :

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, *, id: Any) -> Optional[ModelType]:
        """
        通过 ID 获取对象
        :param db: Session
        :param id: ID
        :return: 查询到的对象
        """
        return db.query(self.model).filter(self.model.id == id and self.model.is_delete != 1).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> Dict[str, Union[int, Any]]:
        """
        获取 skip-limit 的对象集

        :param db: Session
        :param skip: 起始 (默认值0)
        :param limit: 结束 (默认值100)
        :return: 查询到的对象集
        """
        # list = db.query(self.model).offset(skip).limit(limit).all()
        # count = db.query(func.count(distinct(self.model.id))).scalar()
        # print({'list': list, 'count': count})
        # return db.query(self.model).filter(self.model.is_delete != 1).offset(skip).limit(
        #     limit).all()
        list = db.query(self.model).filter(self.model.is_delete != 1).offset(skip).limit(
            limit).all()
        count = len(list)
        return {'data': list, 'count': count}

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        创建对象
        :param db: Session
        :param obj_in: CreateSchemaType schemas类型
        :return: 模型对象
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        更新对象
        :param db: Session
        :param db_obj: ModelType 模型对象
        :param obj_in: UpdateSchemaType schemas类型
        :param obj_in: Dict[str, Any] 字典数据
        :return: 模型对象
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_is_delete(self, db: Session, *, id: str) -> ModelType:
        """
        通过 ID 修改文件状态为1
        :param db: Session
        :param id: ID
        :return: 删除对象的结果
        """
        obj = db.query(self.model).get(id)
        setattr(obj, 'is_delete', 1)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, id: str) -> ModelType:
        """
        通过 ID 删除对象
        :param db: Session
        :param id: ID
        :return: 删除对象的结果
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
