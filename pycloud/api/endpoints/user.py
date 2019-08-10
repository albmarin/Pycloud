# -*- coding: utf-8 -*-
from fastapi import APIRouter, Body, Depends

from pycloud.core.jwt import get_current_user_authorizer
from pycloud.crud.helpers import check_free_username_and_email
from pycloud.crud.user import update_user
from pycloud.db.database import DBClient, get_db_client
from pycloud.models.user import User, UserInResponse, UserInUpdate

router = APIRouter()


@router.get("/user", response_model=UserInResponse, tags=["users"])
async def retrieve_current_user(user: User = Depends(get_current_user_authorizer())):
    return UserInResponse(user=user)


@router.put("/user", response_model=UserInResponse, tags=["users"])
async def update_current_user(
    user: UserInUpdate = Body(..., embed=True),
    current_user: User = Depends(get_current_user_authorizer()),
    client: DBClient = Depends(get_db_client),
):
    if user.username == current_user.username:
        user.username = None

    if user.email == current_user.email:
        user.email = None

    await check_free_username_and_email(client.conn.pycloud, user.username, user.email)

    db_user = await update_user(client.conn.pycloud, current_user.username, user)
    return UserInResponse(user=User(**db_user.dict(), token=current_user.token))
