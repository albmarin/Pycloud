# -*- coding: utf-8 -*-
import json
from loguru import logger
from fastapi import Depends
from jose import jwt
from six.moves.urllib.request import urlopen
from starlette.requests import Request

from pycloud_api.models.schemas.token import Token
from pycloud_api.settings import Config
from .errors import AuthError
from pycloud_api.models.mongo.base import init_instance

ALGORITHMS = ["RS256"]


# Format error response and append status code
async def get_token_auth_header(request: Request) -> Token:
    """Obtains the Access Token from the Authorization Header or Cookie
    """
    header_authorization: str = request.headers.get("Authorization")
    cookie_authorization: str = request.cookies.get("Authorization")

    auth: str = header_authorization or cookie_authorization

    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            },
            401,
        )

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with" " Bearer",
            },
            401,
        )
    elif len(parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found"}, 401
        )

    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be" " Bearer token",
            },
            401,
        )

    token = parts[1]
    return Token(access_token=token, token_type="JWT")


async def requires_auth(token: Token = Depends(get_token_auth_header)) -> dict:
    jsonurl = urlopen(Config.AUTH0_CLIENT_SECRETS_JSON)
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token.access_token)
    rsa_key = {}

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    if rsa_key:

        try:
            payload = jwt.decode(
                token.access_token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=Config.AUTH0_API_AUDIENCE,
                issuer="https://" + Config.AUTH0_DOMAIN + "/",
            )

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "token is expired"}, 401
            )

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "incorrect claims,"
                    "please check the audience and issuer",
                },
                401,
            )

        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication" " token.",
                },
                401,
            )

        await init_instance(payload)
        return payload

    raise AuthError(
        {"code": "invalid_header", "description": "Unable to find appropriate key"}, 401
    )
