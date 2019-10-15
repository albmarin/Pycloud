# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .endpoints import tenant, user, docs

router = APIRouter()

# Top Level Routes
router.include_router(tenant.router)
router.include_router(user.router)

# Documentation Routes
router.include_router(docs.openapi.router)
