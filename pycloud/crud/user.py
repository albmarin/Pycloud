# -*- coding: utf-8 -*-
from pydantic import EmailStr
from pymongo.database import Database

from pycloud.models.user import UserInCreate, UserInDB, UserInUpdate


async def get_user(db: Database, username: str) -> UserInDB:
    document = db.users.find_one(
        {"username": username},
        {
            "_id": 1,
            "username": 1,
            "salt": 1,
            "hashed_password": 1,
            "bio": 1,
            "image": 1,
            "create_at": 1,
            "update_at": 1,
        },
    )

    if document:
        return UserInDB(**document)


async def get_user_by_email(db: Database, email: EmailStr) -> UserInDB:
    document = db.users.find_one(
        {"email": email},
        {
            "_id": 1,
            "username": 1,
            "email": 1,
            "salt": 1,
            "hashed_password": 1,
            "bio": 1,
            "image": 1,
            "created_at": 1,
            "updated_at": 1,
        },
    )

    if document:
        return UserInDB(**document)


async def create_user(db: Database, user: UserInCreate) -> UserInDB:
    db_user = UserInDB(**user.dict())
    db_user.change_password(user.password)

    document = db.users.insert_one(db_user.dict())
    document = db.users.find_one({"_id": document.inserted_id})

    db_user.id = document["_id"]
    db_user.created_at = document["created_at"]
    db_user.updated_at = document["updated_at"]

    return db_user


async def update_user(db: Database, username: str, user: UserInUpdate) -> UserInDB:
    db_user = await get_user(db, username)

    db_user.username = user.username or db_user.username
    db_user.email = user.email or db_user.email
    db_user.bio = user.bio or db_user.bio
    db_user.image = user.image or db_user.image

    if user.password:
        db_user.change_password(user.password)

    document = db.users.find_one_and_update(
        {"username": username},
        {
            "$set": {
                "username": db_user.username,
                "email": db_user.email,
                "salt": db_user.salt,
                "hashed_password": db_user.hashed_password,
                "bio": db_user.bio,
                "image": db_user.image,
            }
        },
    )

    db_user.updated_at = document["updated_at"]
    return db_user
