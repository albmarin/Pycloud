# -*- coding: utf-8 -*-
import sentry_sdk
from fastapi import FastAPI as _FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from pycloud.api import router as api_router
from pycloud.core.errors import http_422_error_handler, http_error_handler
from pycloud.db.db_utils import close_mongo_connection, connect_to_mongo
from pycloud.settings import Config


class FastAPI(_FastAPI):
    def __init__(self, *args, **kwargs):
        super(FastAPI, self).__init__(*args, **kwargs)

        self.config = Config()

        self.add_middleware(
            CORSMiddleware,
            allow_origins=getattr(Config, "ALLOWED_HOSTS", ["*"]),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.add_exception_handler(HTTPException, http_error_handler)
        self.add_exception_handler(
            HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler
        )
        self.include_router(api_router, prefix=Config.API_V1_STR)


def create_app():
    if Config.SENTRY_DSN:
        sentry_sdk.init(Config.SENTRY_DSN)

    app = FastAPI(title=Config.PROJECT_NAME)
    app.add_event_handler("startup", connect_to_mongo)
    app.add_event_handler("shutdown", close_mongo_connection)

    return app
