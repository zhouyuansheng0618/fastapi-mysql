# -*- coding: utf-8 -*-
# @Author : zhouys
# @Contact:zhouys618@163.com
# @Software : blog_server
# @File : crud_tag
# @Time : 2021/12/22 22:19
from typing import Any, Dict, Union

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from crud.base import CRUDBase
from models.settings import Tag
from schemas.blog import TagUpdate, TagCreate


class CRUDTag(CRUDBase[Tag, TagUpdate, TagCreate]):
    def create(self, db: Session, *, obj_in: TagCreate) -> Tag:
        """
        添加 标签
        """
        db_obj = self.model(**jsonable_encoder(obj_in))  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Tag, obj_in: Union[TagUpdate, Dict[str, Any]]) -> Tag:
        if isinstance(obj_in, dict):
            tag_data = obj_in
        else:
            tag_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=tag_data)


tag = CRUDTag(Tag)
