from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import crud as temperature_crud
from temperature import schemas

from city import crud as city_crud

from dependencies import get_db


router = APIRouter()


@router.get(
    "/temperatures/",
    response_model=list[schemas.Temperature]
)
async def read_temperature(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int = None
):
    if city_id is not None:
        db_city = await city_crud.get_city_by_id(db=db, city_id=city_id)
        if db_city is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found"
            )

    return await temperature_crud.get_all_temperatures(db=db, city_id=city_id)


@router.post(
    "/temperatures/update/",
    status_code=status.HTTP_200_OK
)
async def update_temperature_history(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    await temperature_crud.update_temperatures(db=db)
