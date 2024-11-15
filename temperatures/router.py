from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from depencies import get_db
from temperatures import crud
from temperatures import schemas

router = APIRouter()


@router.post("/temperatures/", response_model=list[schemas.Temperature])
async def create_temperatures(db: AsyncSession = Depends(get_db)):
    result = await crud.create_temperatures_record(db)
    return result


@router.get("/temperatures/")
async def get_temperatures(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    """Fetch temperatures filtered by city_id (optional)."""
    result = await crud.get_temperatures_records(db=db, city_id=city_id)
    if not result:
        raise HTTPException(status_code=404, detail="No temperatures found")
    return result
