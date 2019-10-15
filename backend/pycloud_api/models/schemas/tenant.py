# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr, UrlStr

from .dbmodel import DBModelMixin
from .rwmodel import RWModel


class TenantBase(RWModel):
    name: str = None
    email: EmailStr = None
    domain: str = None
    bio: Optional[str] = ""
    logo: Optional[UrlStr] = None
    disabled: bool = False


class TenantInDB(DBModelMixin, TenantBase):
    pass


class Tenant(TenantBase):
    pass


class TenantInResponse(BaseModel):
    tenant: Tenant


class TenantInUpdate(TenantBase):
    pass
