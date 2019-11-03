# -*- coding: utf-8 -*-
from .tenant import Tenant
from .user import User


async def ensure_indexes():
    # Make sure that unique indexes are created
    await Tenant.ensure_indexes()


async def ensure_lazy_indexes():
    await User.ensure_indexes()
