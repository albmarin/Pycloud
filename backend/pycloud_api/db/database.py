# -*- coding: utf-8 -*-
from motor.motor_asyncio import AsyncIOMotorClient

from pycloud_api.settings import Config


class DBClient:
    conn: AsyncIOMotorClient = None
    tenant_db: str = None


client = DBClient()


async def get_db_client():
    return client


def get_mongo_db(db_name: str = None):
    client.conn = AsyncIOMotorClient(str(Config.MONGO_URI))
    return client.conn[db_name]
