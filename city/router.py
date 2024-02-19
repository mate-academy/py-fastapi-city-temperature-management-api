from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityList])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_city(db=db)
