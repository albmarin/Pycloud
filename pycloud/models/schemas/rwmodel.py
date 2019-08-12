# -*- coding: utf-8 -*-
from datetime import datetime, timezone

from bson import ObjectId
from pydantic import BaseConfig, BaseModel


class RWModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_alias = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            ObjectId: lambda obj_id: str(obj_id),
        }
