# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends

from pycloud.crud.tag import fetch_all_tags
from pycloud.db.database import DBClient, get_db_client
from pycloud.models.tag import TagsList

router = APIRouter()


@router.get("/tags", response_model=TagsList, tags=["tags"])
async def get_all_tags(client: DBClient = Depends(get_db_client)):
    tags = await fetch_all_tags(client.conn.pycloud)
    return TagsList(tags=[tag.tag for tag in tags])
