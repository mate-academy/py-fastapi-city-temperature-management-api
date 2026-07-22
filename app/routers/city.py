from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from app.city import crud, schemas, models
from app.dependencies import get_db, DatabaseCityIdParams
from app import utils

router = APIRouter()


@router.get("/cities", response_model=list[schemas.CityModel])
async def get_all_cities(db: AsyncSession = Depends(get_db)) -> list[models.City]:
    return await crud.get_city_list(db)


@router.get("/cities/{city_id}", response_model=schemas.CityModel)
async def get_single_city(params: DatabaseCityIdParams) -> models.City:
    return await utils.handle_city_not_found(
        params["city_id"],
        params["db"]
    )


@router.post("/cities", response_model=schemas.CityModel)
async def write_city(
    data: schemas.CityCreateUpdateModel,
    db: AsyncSession = Depends(get_db)
) -> models.City:
    city = await crud.get_city_by_name(db, data.name)

    if city:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists"
        )


    return await crud.create_city(db, data)


@router.put("/cities/{city_id}", response_model=schemas.CityModel)
async def modify_single_city(
    data: schemas.CityCreateUpdateModel,
    params: DatabaseCityIdParams
) -> models.City:
    await utils.handle_city_not_found(params["city_id"], params["db"])
    await utils.handle_city_exists(data, params["db"], params["city_id"])

    return await crud.completely_update_city_by_id(
        db=params["db"],
        data=data,
        id_=params["city_id"]
    )


@router.delete("/cities/{city_id}")
async def destroy_city(params: DatabaseCityIdParams) -> None:
    await utils.handle_city_not_found(
        params["city_id"],
        params["db"]
    )
    await crud.delete_city_by_id(params["db"], params["city_id"])
