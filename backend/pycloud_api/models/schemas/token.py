# -*- coding: utf-8 -*-
from typing import List

from .rwmodel import RWModel


class Token(RWModel):
    access_token: str
    token_type: str


class TokenData(RWModel):
    username: str = None
    email: str = None
    scopes: List[str] = []
