# -*- coding: utf-8 -*-

from typing import List, Tuple, Optional

from bson.objectid import ObjectId
from loguru import logger

from pycloud_api.models.mongo.tenant import Tenant
from pycloud_api.models.schemas.tenant import TenantBase, TenantInDB, TenantInUpdate


async def get_tenant(query: dict = None) -> TenantInDB:
    query = query or {}
    document = await Tenant.find_one(query)

    if document:
        return TenantInDB(**document.dump())


async def get_tenants(
    query: Optional[dict] = None, page: Optional[int] = 1, limit: int = 10
) -> Tuple[List[TenantInDB], int, bool]:
    query = query or {}

    total = await Tenant.count_documents(query)
    cursor = Tenant.find(query, limit=limit, skip=(page - 1) * limit)
    has_next = total > (limit * page)

    return (
        [TenantInDB(**document.dump()) for document in (await cursor.to_list(limit))],
        total,
        has_next,
    )


async def get_tenant_by_name(name: str) -> TenantInDB:
    document = await Tenant.find_one({"name": name})

    if document:
        return TenantInDB(**document.dump())


async def get_tenant_by_id(obj_id: str) -> TenantInDB:
    document = await Tenant.find_one({"id": ObjectId(obj_id)})

    if document:
        return TenantInDB(**document.dump())


async def get_tenant_by_domain(domain: str) -> TenantInDB:
    document = await Tenant.find_one({"domain": domain})

    if document:
        return TenantInDB(**document.dump())


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
