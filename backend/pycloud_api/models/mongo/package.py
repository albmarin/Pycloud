# -*- coding: utf-8 -*-
from umongo import fields

from .base import LazyBaseModel, lazy_instance
from .user import User


@lazy_instance.register
class Package(LazyBaseModel):
    name = fields.StringField(required=True, unique=True)
    summary = fields.StringField(required=False)
    maintainers = fields.ListField(fields.ReferenceField(User))


@lazy_instance.register
class Release(LazyBaseModel):
    description = fields.StringField(required=True, default="")
    download_url = fields.URLField(required=False)
    home_page: fields.URLField(required=False)
    version: fields.StringField(required=True)
    keywords: fields.StringField(required=False)

    package = fields.ReferenceField(Package)
