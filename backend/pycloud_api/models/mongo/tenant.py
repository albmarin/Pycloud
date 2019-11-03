# -*- coding: utf-8 -*-

from umongo import fields

from .base import BaseModel, instance, db


@instance.register
class Tenant(BaseModel):
    name = fields.StringField(required=True, unique=True)
    email = fields.EmailField(required=True, unique=True)
    domain = fields.StringField(required=True, unique=True)
    bio = fields.StringField(required=False, default="")
    logo = fields.URLField(required=False, default=None)
    disabled = fields.BooleanField(required=False, default=False)

    class Meta:
        collection = db.tenants
