# -*- coding: utf-8 -*-
import datetime

from bson.objectid import ObjectId
from loguru import logger
from pycloud_api.common.structures import Struct
from umongo import Instance, Document, fields, MotorAsyncIOInstance
from umongo.data_objects import List as UMongoList
from umongo.frameworks.motor_asyncio import MotorAsyncIOReference

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

    class Meta:
        allow_inheritance = True
        abstract = True
        indexes = ("#id", "created_at", "updated_at")

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

    async def fetch_references(self) -> Struct:
        logger.debug(f"Fetching References for {self.__class__.__name__}...")
        loaded_doc = Struct(**self.dump())

        async def _fetch_reference(_field: MotorAsyncIOReference):
            _fetched_field = await _field.fetch()
            return Struct(**_fetched_field.dump())

            # TODO find a way to speed up this piece of code to allow for a fully loaded document
            # _fetched_field = await _fetched_field.fetch_references()
            # return _fetched_field

        for field in self._data.items():
            if isinstance(field[1], MotorAsyncIOReference):
                fetched_field = await _fetch_reference(field[1])
                setattr(loaded_doc, field[0], fetched_field)

            elif isinstance(field[1], UMongoList):
                list_field = [
                    await _fetch_reference(item)
                    for item in field[1]
                    if isinstance(item, MotorAsyncIOReference)
                ]

                setattr(loaded_doc, field[0], list_field)

        return loaded_doc


BaseModel = instance.register(Base)
LazyBaseModel = lazy_instance.register(Base)


async def init_instance(payload: dict = None):
    domain = payload[f"{Config.AUTH0_API_AUDIENCE}/app_metadata"]["tenant"][
        "domain"
    ].replace(".", "_")
    client.tenant_db = f"{Config.PROJECT_NAME.lower()}_{domain.lower()}"

    db = get_mongo_db(client.tenant_db)
    lazy_instance.init(db)
