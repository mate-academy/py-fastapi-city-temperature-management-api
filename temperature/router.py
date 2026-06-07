from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)], city_id: int | None = None
):
    return await crud.get_temperature_list(db=db, city_id=city_id)


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
async def update_temperatures(db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        return await crud.update_temperatures(db=db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
