from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from settings import settings
from temperature import crud, schemas

router = APIRouter(prefix=f"{settings.API_PREFIX}/temperatures")

@router.post("/update/", response_model=dict)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    result = await crud.update_temperatures(db=db)
    return result

@router.get("/", response_model=list[schemas.Temperature])
async def read_all_temperatures(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_temperatures(db=db, city_id=city_id)
