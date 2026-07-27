from typing import Annotated

from fastapi import APIRouter, Depends, Query
from temperature import schemas, crud
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_all_temperatures(
    db: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    city_id: Annotated[int | None, Query()] = None,
):
    return await crud.get_temperature_list(
        db=db, limit=limit, skip=skip, city_id=city_id
    )


@router.post("/temperatures/update/", response_model=None)
async def update_all_temperatures(db: SessionDep):
    await crud.update_temperature_list(db=db)
    return {"message": "Temperatures updated successfully"}
