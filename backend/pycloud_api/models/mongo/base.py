# -*- coding: utf-8 -*-
import datetime

from bson.objectid import ObjectId
from umongo import Instance, Document, fields, MotorAsyncIOInstance

from pycloud_api.db.database import client, get_mongo_db
from pycloud_api.settings import Config

lazy_instance = MotorAsyncIOInstance()

db = get_mongo_db(f"{Config.PROJECT_NAME.lower()}_default")
instance = Instance(db)


class Base(Document):
    id = fields.ObjectIdField(
        required=True, attribute="_id", default=ObjectId, allow_none=True
    )
    created_at = fields.DateTimeField(allow_none=True)
    updated_at = fields.DateTimeField(default=datetime.datetime.now, allow_none=True)

    @staticmethod
    def _super(tmpl, self):
        return self._get_impl_from_tmpl(tmpl)

    def _get_impl_from_tmpl(self, tmpl):
        return self.opts.instance.retrieve_document(tmpl)

    async def pre_insert(self):
        if not self.id:
            self.id = ObjectId()

        if not self.created_at:
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()

    async def pre_update(self):
        if self.is_modified():
            self.updated_at = datetime.datetime.now()

    def dict_update(self, **kwargs):
        for k, v in kwargs.items():
            if getattr(self, k):
                self[k] = v

    class Meta:
        allow_inheritance = True
        abstract = True
        indexes = ("#id", "created_at", "updated_at")


BaseModel = instance.register(Base)
LazyBaseModel = lazy_instance.register(Base)


async def init_instance(payload: dict = None):
    domain = payload[f"{Config.AUTH0_API_AUDIENCE}/app_metadata"]["tenant"][
        "domain"
    ].replace(".", "_")
    client.tenant_db = f"{Config.PROJECT_NAME.lower()}_{domain.lower()}"

    db = get_mongo_db(client.tenant_db)
    lazy_instance.init(db)
