# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .endpoints import auth, user, tag

router = APIRouter()

router.include_router(auth.router)
router.include_router(user.router)
router.include_router(tag.router)
