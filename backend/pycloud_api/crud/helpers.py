# -*- coding: utf-8 -*-
import contextlib
import re

from bson.errors import InvalidId
from bson.objectid import ObjectId
from dateutil import parser as date_parser
from pydantic import UrlStr, BaseModel
from typing import Optional, List, Tuple, Any
from umongo import instance
from pymongo import ASCENDING, DESCENDING
from pycloud_api.models.schemas.response import (
    ResponseList,
    ResponseListLink,
    ResponseListLinks,
    ResponseListMeta,
)


async def _parse_query_values(query: dict = None) -> dict:
    query = query or {}

    async def _parse_values(key, val):
        if isinstance(val, dict):
            await _parse_query_values(val)

        with contextlib.suppress(Exception):
            val = date_parser.parse(val)

        with contextlib.suppress(InvalidId):
            val = ObjectId(str(val))

        query[key] = val

    _ = [await _parse_values(k, v) for k, v in query.items()]

    return query


async def get_document(
    model: instance, model_schema, query: dict = None, fetch_references: bool = False
) -> Optional[BaseModel]:
    query = await _parse_query_values(query)
    document = await model.find_one(query)

    if fetch_references:
        loaded_doc = await document.fetch_references()
        return await loaded_doc.dump()

    if document:
        return model_schema(**document.dump())

    return None


async def get_document_list(
    model: instance,
    model_schema,
    query: Optional[dict] = None,
    page: Optional[int] = 1,
    limit: int = 10,
    sort: str = None,
    fetch_references: bool = False,
) -> Tuple[List[Any], int, bool]:
    query = await _parse_query_values(query)
    total = await model.count_documents(query)
    cursor = model.find(query, limit=limit, skip=(page - 1) * limit)
    has_next = total > (limit * page)

    if sort:
        sort_order = {"+": ASCENDING, "-": DESCENDING}.get(sort[0], ASCENDING)
        sort_by = "{}".format(sort[1:] if sort[0] in ["+", "-"] else sort)

        cursor = cursor.sort([(sort_by, sort_order)])

    if fetch_references:

        async def _fetcher(document):
            loaded_doc = await document.fetch_references()
            dumped_doc = await loaded_doc.dump()
            return dumped_doc

        return (
            [await _fetcher(document) for document in (await cursor.to_list(limit))],
            total,
            has_next,
        )

    return (
        [model_schema(**document.dump()) for document in (await cursor.to_list(limit))],
        total,
        has_next,
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
