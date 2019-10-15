# -*- coding: utf-8 -*-
from typing import Optional, List

from pydantic import UrlStr, constr

from .dbmodel import DBModelMixin, ObjectIdStr
from .rwmodel import RWModel
from .user import UserInDB


class Package(RWModel):
    name: str
    summary: Optional[str] = ""
    maintainers: Optional[List[UserInDB]]


class PackageInDB(DBModelMixin, Package):
    pass


class Release(RWModel):
    description: str
    download_url: Optional[UrlStr]
    home_page: Optional[UrlStr]
    version: constr(max_length=80)
    keywords: constr(max_length=255)

    package: Optional[ObjectIdStr] = None


class ReleaseInDB(DBModelMixin, Release):
    pass
