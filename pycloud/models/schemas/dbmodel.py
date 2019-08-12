# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, Schema


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")
        return str(v)


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Schema(..., alias="createdAt")
    updated_at: Optional[datetime] = Schema(..., alias="updatedAt")


class DBModelMixin(DateTimeModelMixin):
    id: Optional[ObjectIdStr] = None

    class Config:
        orm_mode = True
