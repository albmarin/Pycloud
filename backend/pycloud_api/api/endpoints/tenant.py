# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import APIRouter, Path, Body, Security
from pycloud_api.crud.helpers import build_list_response
from pycloud_api.crud.tenant import (
    check_free_tenant_name_and_domain,
    create_tenant,
    update_tenant,
    get_tenant_by_id,
    get_tenants,
)
from pycloud_api.crud.user import get_current_user
from pycloud_api.models.schemas.response import ResponseList
from pycloud_api.models.schemas.tenant import Tenant, TenantInUpdate, TenantInResponse
from pycloud_api.models.schemas.user import UserInDB
from pydantic import Json
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED

router = APIRouter()


# @router.post("/login", response_model=UserInResponse, tags=["authentication"])
# async def login(user: User = Body(..., embed=True)):
#     db_user = await get_user_by_email(user.email)
#
#     access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
#     # token = create_access_token(
#     #     data={"username": db_user.username}, expires_delta=access_token_expires
#     # )
#
#     return UserInResponse(user=User(**db_user.dict(), token=token))


@router.post(
    "/tenants",
    response_model=TenantInResponse,
    tags=["tenants", "register"],
    status_code=HTTP_201_CREATED,
)
async def register(tenant: Tenant = Body(..., embed=True)):
    await check_free_tenant_name_and_domain(tenant.name, tenant.domain)

    db_tenant = await create_tenant(tenant)
    return TenantInResponse(tenant=Tenant(**db_tenant.dict()))


@router.get("/tenants", response_model=ResponseList, tags=["tenants"])
async def list_tenants(
    *,
    request: Request,
    limit: int = 10,
    page: Optional[int] = 1,
    q: Optional[Json] = None,
    sort: str = None,
    fetch_references: bool = False,
    current_user: UserInDB = Security(get_current_user, scopes=["read:tenant"]),
):
    result, total, has_next = await get_tenants(q, page, limit, sort, fetch_references)
    return await build_list_response(
        result, limit, page, total, str(request.url), has_next
    )


@router.get("/tenants/{obj_id}", response_model=TenantInResponse, tags=["tenants"])
async def get_tenant(
    obj_id: str,
    current_user: UserInDB = Security(get_current_user, scopes=["read:tenant"]),
):
    tenant_by_id = await get_tenant_by_id(obj_id)
    return TenantInResponse(tenant=Tenant(**tenant_by_id.dict()))


@router.patch("/tenants/{obj_id}", response_model=TenantInResponse, tags=["tenants"])
async def update_tenants(
    *,
    obj_id: str = Path(..., title="The ObjectID of the item to get"),
    tenant: TenantInUpdate = Body(..., embed=True),
    current_user: UserInDB = Security(get_current_user, scopes=["edit:tenant"]),
):
    tenant_by_id = await get_tenant_by_id(obj_id)
    updated_tenant = await update_tenant(tenant_by_id.name, tenant)

    return TenantInResponse(tenant=Tenant(**updated_tenant.dict()))
