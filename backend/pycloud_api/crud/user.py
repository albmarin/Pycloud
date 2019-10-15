# -*- coding: utf-8 -*-
import httpx
from fastapi import Depends, HTTPException
from fastapi.security import SecurityScopes
from jose.exceptions import JWTError
from pydantic import EmailStr
from pydantic import ValidationError
from starlette.status import HTTP_401_UNAUTHORIZED

from pycloud_api.core.auth import requires_auth, get_token_auth_header
from pycloud_api.core.errors import AuthError
from pycloud_api.models.mongo import User
from pycloud_api.models.schemas.token import Token, TokenData
from pycloud_api.models.schemas.user import UserBase, UserInDB
from pycloud_api.models.schemas.user import UserInUpdate
from pycloud_api.settings import Config
from .tenant import get_tenant_by_domain


async def get_user_info(token: Token = Depends(get_token_auth_header)) -> UserBase:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://{Config.AUTH0_DOMAIN}/userinfo",
            headers={"Authorization": f"Bearer {token.access_token}"},
        )

        user_info = resp.json()
        return UserBase(username=user_info["email"], **user_info)


async def get_current_user(
    security_scopes: SecurityScopes,
    payload: dict = Depends(requires_auth),
    user: UserBase = Depends(get_user_info),
) -> UserInDB:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'

    else:
        authenticate_value = f"Bearer"

    credentials_exception = AuthError("Could not validate credentials", status_code=401)

    try:
        email: str = user.email

        if email is None:
            raise credentials_exception

        token_scopes = payload.get("scope", "").split()
        token_data = TokenData(scopes=token_scopes, username=email, email=email)

    except (JWTError, ValidationError):
        raise credentials_exception

    user = await create_user(user)

    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user


async def get_user(username: str) -> UserInDB:
    document = await User.find_one({"username": username})

    if document:
        return UserInDB.from_orm(document)


async def get_user_by_email(email: EmailStr) -> UserInDB:
    document = await User.find_one({"email": email})

    if document:
        return UserInDB.from_orm(document)


async def create_user(user: UserBase) -> UserInDB:
    user_by_email = await get_user_by_email(user.email)
    if user_by_email:
        return user_by_email

    tenant_by_domain = await get_tenant_by_domain(domain=user.email.split("@")[1])

    user.tenant = tenant_by_domain.id
    db_user = UserInDB(**user.dict())

    document = User(**db_user.dict())
    await document.commit()

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

    document = User.objects(username=username).first()
    document.dict_update(**user.dict())
    document.save()

    db_user.updated_at = document["updated_at"]
    return db_user
