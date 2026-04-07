from typing import Annotated

from fastapi import APIRouter, Query, status

import crud
import schemas
from database import DbSession
from services.weather import fetch_all_temperatures

router = APIRouter()


@router.post("/update", status_code=status.HTTP_201_CREATED)
async def update_temperatures(db: DbSession) -> list[schemas.TemperatureResponse]:
    return await fetch_all_temperatures(db)


@router.get("/")
async def read_temperatures(
    db: DbSession,
    city_id: Annotated[int | None, Query(ge=1)] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[schemas.TemperatureResponse]:
    return await crud.get_temperatures(db=db, city_id=city_id, skip=skip, limit=limit)
