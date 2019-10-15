# -*- coding: utf-8 -*-
import logging

from motor.motor_asyncio import AsyncIOMotorClient

from pycloud_api.settings import Config
from .database import client


async def connect_to_mongo():
    logging.info("Connecting to database")

    client.conn = AsyncIOMotorClient(str(Config.MONGO_URI))

    logging.info("Connected to database")


async def close_mongo_connection():
    logging.info("Closing connection")

    client.conn.close()

    logging.info("Connection closed")
