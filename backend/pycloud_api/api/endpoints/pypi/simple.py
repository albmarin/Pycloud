# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import APIRouter, File, UploadFile, Security
from loguru import logger
from pydantic import Json
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_400_BAD_REQUEST

from pycloud_api.crud.helpers import build_list_response
from pycloud_api.crud.package import create_release, get_packages
from pycloud_api.crud.user import get_current_user
from pycloud_api.models.schemas.response import ResponseList
from pycloud_api.models.schemas.user import UserInDB

router = APIRouter()


@router.get("/pypi/simple", response_model=ResponseList, tags=["pypi", "packages"])
async def list_packages(
    *,
    request: Request,
    limit: int = 10,
    page: Optional[int] = 1,
    q: Optional[Json] = None,
    sort: str = None,
    fetch_references: bool = False,
    current_user: UserInDB = Security(get_current_user, scopes=["read:package"]),
):
    result, total, has_next = await get_packages(q, page, limit, sort, fetch_references)
    return await build_list_response(
        result, limit, page, total, str(request.url), has_next
    )


@router.post("/pypi/simple", status_code=HTTP_201_CREATED, tags=["pypi", "packages"])
async def upload_package(
    *,
    request: Request,
    content: UploadFile = File(...),
    current_user: UserInDB = Security(get_current_user, scopes=["create:package"]),
):
    form = await request.form()
    action = form.get(":action")

    if action != "file_upload":
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Method is not supported."
        )

    try:
        await create_release(form, content)

    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Could not upload release."
        )
