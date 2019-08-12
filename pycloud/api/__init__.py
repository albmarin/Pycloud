# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .endpoints import auth, user, tag, simple

router = APIRouter()

router.include_router(auth.router)
router.include_router(user.router)
router.include_router(tag.router)
router.include_router(simple.router)
