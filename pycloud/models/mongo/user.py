# -*- coding: utf-8 -*-
from mongoengine import StringField, EmailField, URLField

from .base import BaseModel


class User(BaseModel):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    bio = StringField(required=False, default="")
    image = URLField(required=False, default=None)

    salt = StringField(required=True)
    hashed_password = StringField(required=True)

    meta = {"collection": "users"}
