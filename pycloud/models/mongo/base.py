# -*- coding: utf-8 -*-
import datetime
from typing import Dict

from mongoengine import Document, DateTimeField


class BaseModel(Document):
    created_at = DateTimeField()
    updated_at = DateTimeField(default=datetime.datetime.now)

    meta = {"abstract": True}

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()

        self.updated_at = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

    def dict_update(self, **kwargs):
        for k, v in kwargs.items():
            if getattr(self, k):
                self[k] = v
