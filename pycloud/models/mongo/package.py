# -*- coding: utf-8 -*-
from mongoengine import StringField, URLField, ObjectIdField, ListField
from .base import BaseModel


class Package(BaseModel):
    name = StringField(max_length=255, required=True, unique=True)
    summary = StringField(max_length=255, required=False)
    maintainers = ListField(ObjectIdField)

    meta = {"collection": "packages"}


class Release(BaseModel):
    description = StringField(required=True, default="")
    download_url = URLField(required=False)
    home_page = URLField(required=False)
    version = StringField(max_length=80, required=True)
    keywords = StringField(max_length=255, required=False)
    package = ObjectIdField(required=True)

    meta = {"collection": "releases"}
