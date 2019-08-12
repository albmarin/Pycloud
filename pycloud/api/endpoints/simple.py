# -*- coding: utf-8 -*-
from fastapi import APIRouter, File, UploadFile, Depends
from loguru import logger
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from pycloud.db.database import DBClient, get_db_client
from pycloud.crud.package import create_release

router = APIRouter()


@router.get("/simple")
async def list_packages():
    return {"blue": "purple"}


@router.post("/simple", status_code=HTTP_201_CREATED)
async def upload_package(request: Request, content: UploadFile = File(...)):
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
