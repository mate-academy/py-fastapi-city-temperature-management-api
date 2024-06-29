from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependences import DB_DEPENDENCY

router = APIRouter()


@router.post("/city/", response_model=schemas.CityRead)
async def post_list_city(
        city: schemas.CityBase,
        db: AsyncSession = DB_DEPENDENCY
):
    return await crud.post_list_city(db, city)


@router.get("/city/", response_model=list[schemas.CityRead])
async def get_list_city(db: AsyncSession = DB_DEPENDENCY):
    return await crud.get_list_city(db)


@router.get("/city/{city_pk}/", response_model=schemas.CityRead)
async def get_detail_city(city_pk: int, db: AsyncSession = DB_DEPENDENCY):
    return await crud.get_detail_city(db, city_pk)


@router.delete("/city/{city_pk/", status_code=204)
async def delete_detail_city(city_pk: int, db: AsyncSession = DB_DEPENDENCY):
    await crud.delete_detail_city(db, city_pk)


@router.patch("/city/{city_pk/", response_model=schemas.CityRead)
async def patch_detail_city(
        city: schemas.CityPatch,
        city_pk: int,
        db: AsyncSession = DB_DEPENDENCY
):
    return await crud.update_detail_city(db, city_pk, city)
