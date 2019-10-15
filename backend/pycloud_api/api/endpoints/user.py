# -*- coding: utf-8 -*-
from fastapi import APIRouter, Body, Security

from pycloud_api.crud.helpers import check_free_username_and_email
from pycloud_api.crud.tenant import get_tenant_by_id
from pycloud_api.crud.user import get_current_user
from pycloud_api.models.schemas.tenant import Tenant, TenantInResponse
from pycloud_api.models.schemas.user import User, UserInDB, UserInResponse, UserInUpdate

router = APIRouter()


@router.get("/users/me", response_model=UserInResponse, tags=["users"])
async def retrieve_current_user(
    current_user: UserInDB = Security(get_current_user, scopes=["read:profile"])
):
    return UserInResponse(user=User(**current_user.dict()))


@router.put("/users/me", response_model=UserInResponse, tags=["users"])
async def update_current_user(
    user: UserInUpdate = Body(..., embed=True),
    current_user: UserInDB = Security(get_current_user, scopes=["edit:profile"]),
):
    if user.username == current_user.username:
        user.username = None

    if user.email == current_user.email:
        user.email = None

    await check_free_username_and_email(user.username, user.email)
    return UserInResponse(user=User(**current_user.dict()))


@router.get("/users/me/tenant", response_model=TenantInResponse, tags=["users"])
async def retrieve_current_user_tenant(
    current_user: UserInDB = Security(get_current_user, scopes=["read:profile"])
):
    tenant_by_id = await get_tenant_by_id(current_user.tenant)
    return TenantInResponse(tenant=Tenant(**tenant_by_id.dict()))
