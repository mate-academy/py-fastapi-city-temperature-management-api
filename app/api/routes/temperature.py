from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, CommonsDep
from app.temperature import schemas, crud


router = APIRouter()


@router.get("/", response_model=list[schemas.Temperature])
async def get_temperatures(
    commons: CommonsDep,
    city_id: int = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Sequence[schemas.Temperature]:
    if city_id is not None:
        return await crud.get_temperature_by_city_id(
            db=db, city_id=city_id, skip=commons["skip"], limit=commons["limit"]
        )
    return await crud.get_temperatures(
        db=db, skip=commons["skip"], limit=commons["limit"]
    )


@router.post("/update")
async def update_temperatures(
    commons: CommonsDep, db: AsyncSession = Depends(get_db)
) -> None:
    await crud.fetch_and_declare_temperatures(
        db=db, skip=commons["skip"], limit=commons["limit"]
    )
