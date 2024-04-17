from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas, crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
    db: AsyncSession = Depends(get_db),
    city_id: int = Query(None, description="Value of field 1 to filter by"),
):
    return await crud.get_all_temperatures(db=db, city_id=city_id)
