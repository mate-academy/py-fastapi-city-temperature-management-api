from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city.schemas import PaginatedResponse
from dependencies import get_db
from temperature import crud, schemas

router = APIRouter()


@router.get(
    "/temperatures/",
    response_model=PaginatedResponse[schemas.Temperature]
)
async def get_temperature(
        db: AsyncSession = Depends(get_db),
        city_id: int = None,
        page: int = 1,
        size: int = 10,
) -> dict[str, schemas.Temperature]:
    return await crud.get_temperatures(
        db=db, city_id=city_id, page=page, size=size
    )


@router.post(
    "/temperatures/update/",
    response_model=PaginatedResponse[schemas.Temperature]
)
async def update_temperature(
        db: Annotated[AsyncSession, Depends(get_db)]
) -> dict[str, schemas.Temperature]:
    return await crud.fetch_and_update_temperature(db)