# -*- coding: utf-8 -*-
import os
from collections import ChainMap, defaultdict
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret

APP_LOCATION = Path(__file__).parents[1]


class ENVMAP(Enum):
    LOCAL = ".env.local"
    DEVELOPMENT = ".env.dev"
    PRODUCTION = ".env.prod"


load_dotenv(str(APP_LOCATION / ".env"))
settings = ChainMap(os.environ, defaultdict(lambda: None))

env_ = ENVMAP[settings.get("ENV", "DEVELOPMENT").upper()]
load_dotenv(str(APP_LOCATION / env_.value))


class Config(object):
    ENV = settings.get("ENV", "development")
    SECRET_KEY = Secret(settings.get("SECRET_KEY", "its_a_secret_to_everybody"))
    PROJECT_NAME = settings.get("PROJECT_NAME", "Pycloud")
    ALLOWED_HOSTS = CommaSeparatedStrings(settings.get("ALLOWED_HOSTS", ""))

    API_V1_STR = "/api"
    JWT_TOKEN_PREFIX = "Token"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

    MONGO_URI = settings["MONGO_URI"]  # deploying without docker-compose
    MAX_CONNECTIONS_COUNT = int(settings.get("MAX_CONNECTIONS_COUNT", 10))
    MIN_CONNECTIONS_COUNT = int(settings.get("MIN_CONNECTIONS_COUNT", 10))

    SENTRY_DSN = settings["SENTRY_DSN"]
