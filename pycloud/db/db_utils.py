# -*- coding: utf-8 -*-
import logging

from mongoengine import connect

from pycloud.settings import Config
from .database import client


async def connect_to_mongo():
    logging.info("Connecting to database")

    client.conn = connect(
        host=str(Config.MONGO_URI),
        minPoolSize=Config.MIN_CONNECTIONS_COUNT,
        maxPoolSize=Config.MAX_CONNECTIONS_COUNT,
    )

    logging.info("Connected to database")


async def close_mongo_connection():
    logging.info("Closing connection")

    client.conn.close()

    logging.info("Connection closed")
