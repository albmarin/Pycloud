# -*- coding: utf-8 -*-
import os
from collections import ChainMap, defaultdict
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from starlette.datastructures import CommaSeparatedStrings, Secret

APP_LOCATION = Path(__file__).parents[1]


class ENVMAP(str, Enum):
    env = ".env"
    local = ".env.local"
    development = ".env.dev"
    production = ".env.prod"


settings = ChainMap(os.environ, defaultdict(lambda: None))

try:
    load_dotenv(str(APP_LOCATION / ENVMAP.env.value))

    env_ = ENVMAP[settings.get("ENV", "development").lower()]
    load_dotenv(str(APP_LOCATION / env_.value))
    settings = ChainMap(os.environ, defaultdict(lambda: None))

except FileNotFoundError:
    logger.warning("No environment file could be found. Skipping...")


class Config(object):
    ENV = settings.get("ENV", "development")
    SECRET_KEY = Secret(settings.get("SECRET_KEY", "its_a_secret_to_everybody"))
    PROJECT_NAME = settings.get("PROJECT_NAME", "Pycloud")
    ALLOWED_HOSTS = CommaSeparatedStrings(settings.get("ALLOWED_HOSTS", "*"))

    API_V1_STR = "/api"
    JWT_TOKEN_PREFIX = "Token"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

    AUTH0_DOMAIN = settings.get("AUTH0_DOMAIN")
    AUTH0_API_AUDIENCE = settings.get("AUTH0_API_AUDIENCE")

    AUTH0_CLIENT_ID = settings.get("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = settings.get("AUTH0_CLIENT_SECRET")
    AUTH0_CLIENT_SECRETS_JSON = settings.get("AUTH0_CLIENT_SECRETS_JSON")
    AUTH0_SCOPE = settings.get("AUTH0_SCOPE", "openid profile email read:docs")

    SWAP_TOKEN_ENDPOINT = "/swap_token"
    SUCCESS_ROUTE = "/users/me"
    ERROR_ROUTE = "/login_error"

    AWS_ACCESS_KEY_ID = settings["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = settings["AWS_SECRET_ACCESS_KEY"]
    AWS_S3_BUCKET_NAME = settings["AWS_S3_BUCKET_NAME"]

    MONGO_URI = settings["MONGO_URI"]  # deploying without docker-compose
    MAX_CONNECTIONS_COUNT = int(settings.get("MAX_CONNECTIONS_COUNT", 10))
    MIN_CONNECTIONS_COUNT = int(settings.get("MIN_CONNECTIONS_COUNT", 10))

    SENTRY_DSN = settings["SENTRY_DSN"]

    def get(self, item, default=None):
        return getattr(self, item, default)
