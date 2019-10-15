# -*- coding: utf-8 -*-
from typing import Optional, List

from pydantic import BaseModel, UrlStr


class ResponseListLink(BaseModel):
    href: UrlStr
    title: str


class ResponseListLinks(BaseModel):
    last: Optional[ResponseListLink]
    next: Optional[ResponseListLink]
    self: ResponseListLink


class ResponseListMeta(BaseModel):
    limit: int
    page: int
    total: int


class ResponseList(BaseModel):
    items: List = []
    links: Optional[ResponseListLinks] = {}
    meta: ResponseListMeta
