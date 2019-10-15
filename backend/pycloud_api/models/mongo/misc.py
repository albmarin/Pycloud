# -*- coding: utf-8 -*-
import datetime

from bson.objectid import ObjectId
from npyi import npi
from umongo import EmbeddedDocument, fields, validate

from .base import LazyBaseModel, lazy_instance, db


@lazy_instance.register
class Address(EmbeddedDocument):
    street1 = fields.StringField(required=True)
    street2 = fields.StringField(default=None, allow_none=True)
    city = fields.StringField(required=True)
    state = fields.StringField(required=True)
    zip = fields.IntegerField(required=True)


@lazy_instance.register
class Phone(EmbeddedDocument):
    number = fields.IntegerField(required=True)
    description = fields.StringField(default=None, allow_none=True)


@lazy_instance.register
class Contact(EmbeddedDocument):
    name = fields.StringField(required=True)
    relationship = fields.StringField(required=True)

    address = fields.EmbeddedField(Address, allow_none=True)
    phone1 = fields.EmbeddedField(Phone, required=True)
    phone2 = fields.EmbeddedField(Phone, allow_none=True)
