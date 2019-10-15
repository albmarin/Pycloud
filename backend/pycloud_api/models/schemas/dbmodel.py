# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Schema

from .misc import ObjectIdStr


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Schema(..., alias="createdAt")
    updated_at: Optional[datetime] = Schema(..., alias="updatedAt")


class DBModelMixin(DateTimeModelMixin):
    id: Optional[ObjectIdStr] = None

    class Config:
        orm_mode = True
