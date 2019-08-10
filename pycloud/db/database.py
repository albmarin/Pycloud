# -*- coding: utf-8 -*-
from pymongo import MongoClient


class DBClient:
    conn: MongoClient = None


client = DBClient()


async def get_db_client():
    return client
