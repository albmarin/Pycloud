# -*- coding: utf-8 -*-

from enum import Enum

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel
from typing import Optional


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


class Gender(str, Enum):
    male = "M"
    female = "F"


class Address(BaseModel):
    street1: str
    street2: Optional[str] = None
    city: str
    state: str
    zip: int


class Phone(BaseModel):
    number: int
    description: Optional[str] = None


class Contact(BaseModel):
    name: str
    relationship: str

    address: Optional[Address]
    phone1: Phone
    phone2: Optional[Phone]
