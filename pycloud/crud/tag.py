# -*- coding: utf-8 -*-
from typing import List

from pymongo.database import Database

from pycloud.models.tag import TagInDB


async def fetch_all_tags(db: Database) -> List[TagInDB]:
    tags = []
    documents = db.tags.find({}, {"_id": 1, "name": 1, "created_at": 1, "update_at": 1})

    for doc in documents:
        tags.append(TagInDB(**doc))

    return tags


async def create_tags_that_not_exist(db: Database, tags: List[str]):
    for tag in tags:
        db.tags.update({"name": tag}, {"$set": {"name": tag}}, upsert=True)
