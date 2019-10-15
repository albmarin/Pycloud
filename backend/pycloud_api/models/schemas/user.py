# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr, UrlStr

from .misc import ObjectIdStr
from .dbmodel import DBModelMixin
from .rwmodel import RWModel


class UserBase(RWModel):
    username: str
    email: EmailStr
    name: Optional[str] = None
    bio: Optional[str] = ""
    picture: Optional[UrlStr] = None
    disabled: bool = False

    tenant: Optional[ObjectIdStr] = None


class UserInDB(DBModelMixin, UserBase):
    tenant: ObjectIdStr


class User(UserBase):
    token: Optional[str] = None


class UserInResponse(BaseModel):
    user: User


class UserInUpdate(RWModel):
    username: str
    email: EmailStr
    name: Optional[str] = None
    bio: Optional[str] = ""
    picture: Optional[UrlStr] = None
    disabled: bool = None
