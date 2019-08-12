# -*- coding: utf-8 -*-
from pydantic import EmailStr
from pymongo.database import Database

from pycloud.models.mongo.user import User
from pycloud.models.schemas.user import UserInCreate, UserInDB, UserInUpdate


async def get_user(username: str) -> UserInDB:
    document = User.objects(username=username).first()

    if document:
        return UserInDB.from_orm(document)


async def get_user_by_email(email: EmailStr) -> UserInDB:
    document = User.objects(email=email).first()

    if document:
        return UserInDB.from_orm(document)


async def create_user(user: UserInCreate) -> UserInDB:
    db_user = UserInDB(**user.dict())
    db_user.change_password(user.password)

    document = User(**db_user.dict())
    document.save()

    db_user.id = document.id
    db_user.created_at = document.created_at
    db_user.updated_at = document.updated_at

    return db_user


async def update_user(username: str, user: UserInUpdate) -> UserInDB:
    db_user = await get_user(username)

    db_user.username = user.username or db_user.username
    db_user.email = user.email or db_user.email
    db_user.bio = user.bio or db_user.bio
    db_user.image = user.image or db_user.image

    if user.password:
        db_user.change_password(user.password)

    document = User.objects(username=username).first()
    document.dict_update(**user.dict())
    document.save()

    db_user.updated_at = document["updated_at"]
    return db_user
