# -*- coding: utf-8 -*-
# @Author : zhouys
# @Contact:zhouys618@163.com
# @Software : blog_server
# @File : blog_tag
# @Time : 2021/12/21 22:13
from typing import Any, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from common import deps, response_code
from models.blog import BlogTag, Category
from models.settings import Tag
from schemas.blog import CategoryCreate, CategoryUpdate, TagCreate, TagUpdate

router = APIRouter()


@router.post("/create_category", summary="创建文章分类")
def category_create(*, db: Session = Depends(deps.get_db), category_in: CategoryCreate) -> Any:
    get_category = db.query(Category).filter(Category.category_name == category_in.category_name).first()
    if get_category:
        return response_code.resp_4002(message="该分类已经存在")
    add_category = crud.category.create(db, obj_in=category_in)
    return response_code.resp_200(data=add_category, message="文章分类创建成功")


@router.post("/update_category", summary="修改分类名称")
def category_update(*, db: Session = Depends(deps.get_db), category_id: str, category_in: CategoryUpdate) -> Any:
    get_category = crud.category.get(db, id=category_id)
    if not get_category:
        return response_code.resp_4002(message="没有该分类")
    alter_category = crud.category.update(db, db_obj=get_category, obj_in=category_in)
    return response_code.resp_200(data=alter_category, message="修改成功")


@router.get('/get_category', summary="根据id查询or分页查询")
def category_get(*, db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100,
                 category_id: Optional[str] = None) -> Any:
    if category_id:
        get_category = crud.category.get(db, id=category_id)
        if not get_category:
            return response_code.resp_200(message="该id没有数据")
        return response_code.resp_200(data=get_category, message="查询成功")
    get_category_list = crud.category.get_multi(db, skip=skip, limit=limit)
    return response_code.resp_200(data=get_category_list, message="查询成功")


@router.post("/delete_category", summary="删除分类")
def category_delete(*, db: Session = Depends(deps.get_db), category_id: str) -> Any:
    get_category = crud.category.get(db, id=category_id)
    if not get_category:
        return response_code.resp_200(message="没有找到数据")
    crud.category.update_is_delete(db, id=category_id)
    return response_code.resp_200(message="删除成功")


@router.post('/create_tag', summary="创建标签")
def tag_create(*, db: Session = Depends(deps.get_db), tag_in: TagCreate) -> Any:
    get_tag = db.query(Tag).filter(Tag.tag_name == tag_in.tag_name).first()
    if get_tag:
        return response_code.resp_200(message="该分类已存在")
    add_tag = crud.tag.create(db, obj_in=tag_in)
    return response_code.resp_200(data=add_tag, message="标签创建成功")


@router.post("/update_tag", summary="修改分类名称")
def tag_update(*, db: Session = Depends(deps.get_db), tag_id: str, tag_in: TagUpdate) -> Any:
    get_tag = crud.tag.get(db, id=tag_id)
    if not get_tag:
        return response_code.resp_4002(message="没有该分类")
    alter_tag = crud.tag.update(db, db_obj=get_tag, obj_in=tag_in)
    return response_code.resp_200(data=alter_tag, message="修改成功")


@router.get('/get_tag', summary="根据id查询or分页查询")
def tag_get(*, db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100,
            tag_id: Optional[str] = None) -> Any:
    if tag_id:
        get_tag = crud.tag.get(db, id=tag_id)
        if not get_tag:
            return response_code.resp_200(message="该id没有数据")
        return response_code.resp_200(data=get_tag, message="查询成功")
    get_tag_list = crud.tag.get_multi(db, skip=skip, limit=limit)
    return response_code.resp_200(data=get_tag_list, message="查询成功")


@router.post("/delete_tag", summary="删除分类")
def tag_delete(*, db: Session = Depends(deps.get_db), tag_id: str) -> Any:
    get_tag = crud.tag.get(db, id=tag_id)
    if not get_tag:
        return response_code.resp_200(message="没有找到数据")
    crud.tag.update_is_delete(db, id=tag_id)
    return response_code.resp_200(message="删除成功")
