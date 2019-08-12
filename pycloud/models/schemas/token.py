# -*- coding: utf-8 -*-
from .rwmodel import RWModel


class TokenPayload(RWModel):
    username: str = ""
