# -*- coding: utf-8 -*-
import re

from pydantic import EmailStr, UrlStr, BaseModel
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from typing import Optional, List, Dict
from umongo import instance

from pycloud_api.models.schemas.response import (
    ResponseList,
    ResponseListLink,
    ResponseListLinks,
    ResponseListMeta,
)
from .tenant import get_tenant_by_name, get_tenant_by_domain
from .user import get_user, get_user_by_email


async def get_document(
    model: instance, model_schema, query: dict = None
) -> Optional[BaseModel]:
    query = query or {}
    document = await model.find_one(query)

    if document:
        return model_schema(**document.dump())

    return None


async def check_free_username_and_email(
    username: Optional[str] = None, email: Optional[EmailStr] = None
):
    if username:
        user_by_username = await get_user(username)

        if user_by_username:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this username already exists",
            )

    if email:
        user_by_email = await get_user_by_email(email)

        if user_by_email:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this email already exists",
            )


async def check_free_tenant_name_and_domain(
    name: Optional[str] = None, domain: Optional[str] = None
):
    if name:
        tenant_by_name = await get_tenant_by_name(name)

        if tenant_by_name:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A tenant with this name already exists",
            )

    if domain:
        tenant_by_domain = await get_tenant_by_domain(domain)

        if tenant_by_domain:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A tenant with this domain already exists",
            )


async def build_list_response(
    items: List, limit: int, page: int, total: int, self_link: UrlStr, has_next: bool
) -> ResponseList:
    regex = re.compile(r"page=\d", re.IGNORECASE)

    prev_page = None
    next_page = None

    if page > 1:
        prev_page = ResponseListLink(
            href=regex.sub(f"page={page - 1}", self_link), title="prev_page"
        )

    if has_next:
        next_page = ResponseListLink(
            href=regex.sub(f"page={page + 1}", self_link), title="next_page"
        )

    return ResponseList(
        items=items,
        links=ResponseListLinks(
            self=ResponseListLink(href=self_link, title="self"),
            last=prev_page,
            next=next_page,
        ),
        meta=ResponseListMeta(limit=limit, page=page, total=total),
    )
