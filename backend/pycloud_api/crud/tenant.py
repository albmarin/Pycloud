# -*- coding: utf-8 -*-

from typing import List, Tuple, Optional

from bson.objectid import ObjectId
from fastapi import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from pycloud_api.models.mongo.tenant import Tenant
from pycloud_api.models.schemas.tenant import TenantBase, TenantInDB, TenantInUpdate
from .helpers import get_document, get_document_list


async def check_free_tenant_name_and_domain(
    name: Optional[str] = None, domain: Optional[str] = None
):
    if name:
        tenant_by_name = await get_tenant_by_name(name)

        if tenant_by_name:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A tenant with this name already exists",
            )

    if domain:
        tenant_by_domain = await get_tenant_by_domain(domain)

        if tenant_by_domain:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A tenant with this domain already exists",
            )


async def get_tenant(query: dict = None) -> Optional[TenantInDB]:
    return await get_document(Tenant, TenantInDB, query)


async def get_tenants(
    query: Optional[dict] = None,
    page: Optional[int] = 1,
    limit: int = 10,
    sort: str = None,
    fetch_references: bool = False,
) -> Tuple[List[TenantInDB], int, bool]:
    return await get_document_list(
        Tenant, TenantInDB, query, page, limit, sort, fetch_references
    )


async def get_tenant_by_name(name: str) -> Optional[TenantInDB]:
    return await get_document(Tenant, TenantInDB, query={"name": name})


async def get_tenant_by_id(obj_id: str) -> Optional[TenantInDB]:
    return await get_document(Tenant, TenantInDB, query={"id": ObjectId(obj_id)})


async def get_tenant_by_domain(domain: str) -> Optional[TenantInDB]:
    return await get_document(Tenant, TenantInDB, query={"domain": domain})


async def create_tenant(tenant: TenantBase) -> TenantInDB:
    tenant_by_domain = await get_tenant_by_domain(tenant.domain)
    if tenant_by_domain:
        return tenant_by_domain

    db_tenant = TenantInDB(**tenant.dict())
    document = Tenant(**db_tenant.dict())

    await document.commit()
    return TenantInDB(**document.dump())


async def update_tenant(name: str, tenant: TenantInUpdate) -> TenantInDB:
    db_tenant = await get_tenant_by_name(name)
    db_tenant = db_tenant.copy(update=tenant.dict(skip_defaults=True))

    document = await Tenant.find_one({"name": name})
    document.dict_update(**db_tenant.dict())

    await document.commit()
    return TenantInDB(**document.dump())
