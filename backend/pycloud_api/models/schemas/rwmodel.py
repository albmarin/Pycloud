# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from pydantic import BaseConfig, BaseModel

from .misc import ObjectIdStr


class RWModel(BaseModel):
    id: Optional[ObjectIdStr] = None

    class Config(BaseConfig):
        allow_population_by_alias = True
        use_enum_values = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            ObjectId: lambda obj_id: str(obj_id),
        }
