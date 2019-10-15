# -*- coding: utf-8 -*-
from umongo import fields

from .base import LazyBaseModel, lazy_instance


@lazy_instance.register
class User(LazyBaseModel):
    username = fields.StringField(required=True, unique=True)
    email = fields.EmailField(required=True, unique=True)
    name = fields.StringField(required=False, default="")
    bio = fields.StringField(required=False, default="")
    picture = fields.URLField(required=False, default=None)
    disabled = fields.BooleanField(required=False, default=False)

    tenant = fields.ObjectIdField(required=True)
