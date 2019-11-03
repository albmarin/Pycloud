# -*- coding: utf-8 -*-
from collections.abc import Iterable

from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import (
    validation_error_definition,
    validation_error_response_definition,
)
from loguru import logger
from marshmallow.exceptions import ValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


async def default_error_handler(request: Request, exc: Exception):
    return logger.error(exc)


async def auth_error_handler(request: Request, exc: AuthError) -> JSONResponse:
    return JSONResponse({"errors": [exc.error]}, status_code=exc.status_code)


async def validation_error_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    return JSONResponse(
        {"errors": [exc.messages]}, status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]})


async def http_422_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handler for 422 error to transform default pydantic error object to gothinkster format
    """

    errors = {"body": []}

    if isinstance(exc.detail, Iterable) and not isinstance(
        exc.detail, str
    ):  # check if error is pydantic's model error
        for error in exc.detail:
            error_name = ".".join(
                error["loc"][1:]
            )  # remove 'body' from path to invalid element
            errors["body"].append({error_name: error["msg"]})
    else:
        errors["body"].append(exc.detail)

    return JSONResponse({"errors": errors}, status_code=HTTP_422_UNPROCESSABLE_ENTITY)


validation_error_definition["properties"] = {
    "body": {"title": "Body", "type": "array", "items": {"type": "string"}}
}

validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": REF_PREFIX + "ValidationError"},
    }
}
