# -*- coding: utf-8 -*-
from typing import List

from .dbmodel import DBModelMixin
from .rwmodel import RWModel


class Tag(RWModel):
    name: str


class TagInDB(DBModelMixin, Tag):
    pass


class TagsList(RWModel):
    tags: List[str] = []
