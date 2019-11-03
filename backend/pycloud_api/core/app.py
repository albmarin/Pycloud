# -*- coding: utf-8 -*-
import sentry_sdk
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI as _FastAPI
from marshmallow.exceptions import ValidationError
from pycloud_api.api import router as api_router
from pycloud_api.core.errors import (
    AuthError,
    default_error_handler,
    auth_error_handler,
    validation_error_handler,
    http_422_error_handler,
    http_error_handler,
)
from pycloud_api.db.db_utils import close_mongo_connection, connect_to_mongo
from pycloud_api.models.mongo import ensure_indexes
from pycloud_api.settings import Config
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def startup_event():
    await connect_to_mongo()
    await ensure_indexes()


class FastAPI(_FastAPI):
    def __init__(self, *args, **kwargs):
        super(FastAPI, self).__init__(*args, **kwargs)

        self.config = Config()
        self.oauth = OAuth(self.config)
        self.auth0 = self.oauth.register(
            "auth0",
            client_id=self.config.AUTH0_CLIENT_ID,
            client_secret=self.config.AUTH0_CLIENT_SECRET,
            api_base_url=f"https://{self.config.AUTH0_DOMAIN}",
            access_token_url=f"https://{self.config.AUTH0_DOMAIN}/oauth/token",
            authorize_url=f"https://{self.config.AUTH0_DOMAIN}/authorize",
            client_kwargs={"scope": self.config.AUTH0_SCOPE},
        )

        self.add_middleware(
            CORSMiddleware,
            allow_origins=getattr(Config, "ALLOWED_HOSTS"),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.add_middleware(SessionMiddleware, secret_key=self.config.SECRET_KEY)

        self.add_event_handler("startup", connect_to_mongo)
        self.add_event_handler("shutdown", close_mongo_connection)

        self.add_exception_handler(Exception, default_error_handler)
        self.add_exception_handler(AuthError, auth_error_handler)
        self.add_exception_handler(ValidationError, validation_error_handler)
        self.add_exception_handler(HTTPException, http_error_handler)
        self.add_exception_handler(
            HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler
        )

        self.include_router(api_router, prefix=Config.API_V1_STR)


def create_app():
    if Config.SENTRY_DSN:
        sentry_sdk.init(Config.SENTRY_DSN)

    app = FastAPI(
        title=Config.PROJECT_NAME, docs_url=None, redoc_url=None, openapi_url=None
    )
    return app
