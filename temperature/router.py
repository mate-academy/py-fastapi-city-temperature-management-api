from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud

router = APIRouter(prefix="/temperatures", tags=["temperatures"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("/", response_model=list[schemas.Temperature])
async def temperatures_get(db: DbSession) -> list[schemas.Temperature]:
    return await crud.get_all_temperatures(db=db)


@router.get("?city_id={city_id}", response_model=schemas.Temperature)
async def temperature_get_in_city(db: DbSession, city_id: int) -> schemas.Temperature | None:
    if not await crud.get_temperature_in_city(db=db, city_id=city_id):
        raise HTTPException(status_code=404, detail="City not found")


@router.post("/update", response_model=schemas.Temperature)
async def fetch_temperature(db: DbSession) -> schemas.Temperature | None:
    return await crud.fetch_temperature(db=db)
