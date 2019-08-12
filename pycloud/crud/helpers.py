# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import EmailStr
from pymongo.database import Database
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .user import get_user, get_user_by_email


async def check_free_username_and_email(
    username: Optional[str] = None, email: Optional[EmailStr] = None
):
    if username:
        user_by_username = await get_user(username)

        if user_by_username:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this username already exists",
            )

    if email:
        user_by_email = await get_user_by_email(email)

        if user_by_email:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this email already exists",
            )
