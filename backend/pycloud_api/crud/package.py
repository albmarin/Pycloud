# -*- coding: utf-8 -*-
from typing import Optional, Tuple, List

from starlette.datastructures import FormData, UploadFile

from pycloud_api.models.mongo.package import Package, Release
from pycloud_api.models.schemas.package import PackageInDB, ReleaseInDB
from .helpers import get_document, get_document_list


async def get_package(query: dict = None) -> Optional[PackageInDB]:
    return await get_document(Package, PackageInDB, query)


async def get_packages(
    query: Optional[dict] = None,
    page: Optional[int] = 1,
    limit: int = 10,
    sort: str = None,
    fetch_references: bool = False,
) -> Tuple[List[PackageInDB], int, bool]:
    return await get_document_list(
        Package, PackageInDB, query, page, limit, sort, fetch_references
    )


async def get_release_by_version(package: PackageInDB, version: str) -> ReleaseInDB:
    return await get_document(
        Release, ReleaseInDB, query={"package": package.id, "version": version}
    )


async def get_package_by_name(name: str) -> PackageInDB:
    return await get_document(Package, PackageInDB, query={"name": name})


async def create_package(name: str, summary: str) -> PackageInDB:
    document = Package(name=name, summary=summary)
    await document.commit()

    return PackageInDB(**document.dump())


async def create_release(data: FormData, content: UploadFile) -> ReleaseInDB:
    package = await get_package_by_name(data["name"])

    if package is None:
        package = await create_package(data["name"], data["summary"])

    release = await get_release_by_version(package, data["version"])

    if release is None:
        db_release = ReleaseInDB(
            description=data.get("description") or None,
            download_url=data.get("download_url") or None,
            home_page=data.get("home_page") or None,
            version=data["version"],
            keywords=data.get("keywords") or None,
            package=package.id,
        )

        document = Release(**db_release.dict())
        await document.commit()

        release = ReleaseInDB(**document.dump())
    return release
