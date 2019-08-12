# -*- coding: utf-8 -*-
from starlette.datastructures import FormData, UploadFile

from pycloud.models.mongo.package import Package, Release
from pycloud.models.schemas.package import PackageInDB, ReleaseInDB


async def create_release(data: FormData, content: UploadFile) -> ReleaseInDB:
    package = await get_package_by_name(data["name"])

    if package is None:
        package = await create_package(data["name"], data["summary"])

    release = await get_release_by_version(package, data["version"])

    if release is None:
        release = ReleaseInDB(
            description=data.get("description") or None,
            download_url=data.get("download_url") or None,
            home_page=data.get("home_page") or None,
            version=data["version"],
            keywords=data.get("keywords") or None,
            package=package.id,
        )

        try:
            document = Release(**release.dict())
            document.save()

            release = ReleaseInDB.from_orm(document)

        except Exception:
            raise

    return release


async def get_release_by_version(package: PackageInDB, version: str) -> ReleaseInDB:
    release = None
    document = Release.objects(package=package.id, version=version).first()

    if document:
        release = ReleaseInDB.from_orm(document)

    return release


async def get_package_by_name(name: str) -> PackageInDB:
    package = None
    document = Package.objects(name=name).first()

    if document:
        package = PackageInDB.from_orm(document)

    return package


async def create_package(name: str, summary: str) -> PackageInDB:
    document = Package(name=name, summary=summary)
    document.save()

    package = PackageInDB.from_orm(document)
    return package
