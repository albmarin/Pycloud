# -*- coding: utf-8 -*-
from datetime import timedelta

from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from pycloud.core.jwt import create_access_token
from pycloud.crud.helpers import check_free_username_and_email
from pycloud.crud.user import create_user, get_user_by_email
from pycloud.db.database import DBClient, get_db_client
from pycloud.models.user import User, UserInCreate, UserInLogin, UserInResponse
from pycloud.settings import Config

router = APIRouter()


@router.post("/users/login", response_model=UserInResponse, tags=["authentication"])
async def login(
    user: UserInLogin = Body(..., embed=True), client: DBClient = Depends(get_db_client)
):
    db_user = await get_user_by_email(client.conn.pycloud, user.email)

    if not db_user or not db_user.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )

    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"username": db_user.username}, expires_delta=access_token_expires
    )

    return UserInResponse(user=User(**db_user.dict(), token=token))


@router.post(
    "/users",
    response_model=UserInResponse,
    tags=["authentication"],
    status_code=HTTP_201_CREATED,
)
async def register(
    user: UserInCreate = Body(..., embed=True),
    client: DBClient = Depends(get_db_client),
):
    await check_free_username_and_email(client.conn.pycloud, user.username, user.email)

    db_user = await create_user(client.conn.pycloud, user)
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"username": db_user.username}, expires_delta=access_token_expires
    )

    return UserInResponse(user=User(**db_user.dict(), token=token))
