from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from temperature import crud, schemas
from dependencies import get_db

router = APIRouter()


@router.get("/temperatures", response_model=list[schemas.Temperature])
async def read_temperatures(
        db: AsyncSession = Depends(get_db),
        city_id: int = None
):
    return await crud.get_all_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/update")
async def update_temperature(db: AsyncSession = Depends(get_db)):
    return await crud.update_all_temperatures(db=db)
