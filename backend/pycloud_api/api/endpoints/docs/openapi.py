# -*- coding: utf-8 -*-
from pycloud_api.crud.user import get_current_user
from pycloud_api.models.schemas.user import UserInDB
from pycloud_api.settings import Config
from fastapi import APIRouter, Security
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from six.moves.urllib.parse import urlencode
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

router = APIRouter()


async def get_host_url(request: Request):
    scheme = request.url.scheme
    host = request.url.hostname
    port = "" if request.url.port is None else f":{request.url.port}"

    return f"{scheme}://{host}{port}"


@router.get("/login", include_in_schema=False)
async def login(request: Request):
    host_url = await get_host_url(request)

    return await request.app.auth0.authorize_redirect(
        request=request,
        redirect_uri=f"{host_url}/api/callback",
        audience=Config.AUTH0_API_AUDIENCE,
    )


@router.get("/logout", include_in_schema=False)
async def logout_and_remove_cookie(request: Request):
    host_url = await get_host_url(request)
    params = {"returnTo": f"{host_url}/api", "client_id": Config.AUTH0_CLIENT_ID}

    response = RedirectResponse(
        url=request.app.auth0.api_base_url + "/v2/logout?" + urlencode(params)
    )
    response.delete_cookie("Authorization", domain=request.url.hostname)
    return response


@router.get("/callback", include_in_schema=False)
async def login_callback(request: Request):
    token = await request.app.auth0.authorize_access_token(request)

    response = RedirectResponse(url="/api/docs")
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token['access_token']}",
        domain=request.url.hostname,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response


@router.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(
    request: Request,
    current_user: UserInDB = Security(get_current_user, scopes=["read:docs"]),
):
    openapi_schema = get_openapi(
        title=request.app.title,
        version=request.app.version,
        openapi_version=request.app.openapi_version,
        description=request.app.description,
        routes=request.app.routes,
        openapi_prefix=request.app.openapi_prefix,
    )

    return JSONResponse(openapi_schema)


@router.get("/docs", include_in_schema=False)
async def get_swagger(
    request: Request,
    current_user: UserInDB = Security(get_current_user, scopes=["read:docs"]),
):
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title=request.app.title + " - Swagger UI",
        oauth2_redirect_url="/api/docs/oauth2-redirect",
        init_oauth=None,
    )


@router.get("/redoc", include_in_schema=False)
async def get_redoc(
    request: Request,
    current_user: UserInDB = Security(get_current_user, scopes=["read:docs"]),
):
    return get_redoc_html(
        openapi_url="/api/openapi.json", title=request.app.title + " - ReDoc"
    )
