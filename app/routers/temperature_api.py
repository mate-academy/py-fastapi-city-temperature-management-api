from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from .temperature import crud, schemas



router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures_in_cities"],
)

ConnectDB = Annotated[AsyncSession, Depends(get_db)]

async def commons_params(db: ConnectDB, skip: int | None = None , limit: int | None = None):
    return {"db":db, "skip": skip, "limit": limit}

Commons = Annotated[dict, Depends(commons_params)]


@router.post("/update", response_model=list[schemas.TemperatureOut])
async def update_temperatures(commons: Commons):
    updated_temperatures = await crud.update_temperatures(db=commons.get("db"),
                                                          skip=commons.get("skip"),
                                                          limit=commons.get("limit"))

    return updated_temperatures

    return temperatures


async def get_temperature_by_city_id(city_id: int, commons: Commons):
    temperatures = await crud.temperature_by_id(db = commons.get("db"), city_id = city_id,
                                                skip = commons.get("skip"), limit = commons.get("limit"))

    return temperatures

@router.delete("/")
async def delete_temperatures(db: ConnectDB):
    await crud.delete_temperatures(db=db)
    return {"message": "Temperatures deleted"}


@router.get("/", response_model=list[schemas.TemperatureOut])
async def get_temperature_by_city_id(commons: Commons, city_id: int | None = None):
    if city_id is None:
        temperatures = await crud.get_temperatures(db=commons.get("db"),
                                                    skip=commons.get("skip"),
                                                    limit=commons.get("limit"))

    else:
        temperatures = await crud.temperature_by_id(db=commons.get("db"), city_id=city_id,
                                                    skip=commons.get("skip"), limit=commons.get("limit"))

    return temperatures