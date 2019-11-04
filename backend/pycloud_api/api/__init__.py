# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .endpoints import tenant, user, docs, pypi

router = APIRouter()

# Top Level Routes
router.include_router(tenant.router)
router.include_router(user.router)

# Documentation Routes
router.include_router(docs.openapi.router)

# PyPi Routes
router.include_router(pypi.simple.router)
