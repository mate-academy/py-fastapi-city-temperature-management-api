from fastapi import Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import schemas as temp_schemas
from temperature import crud as temp_crud
from db.engine import get_db

router = APIRouter()


@router.post("/update/", response_model=list[temp_schemas.TemperatureUpdate])
async def update_temperature(db: AsyncSession = Depends(get_db)):
    return await temp_crud.temperature_update_all(db=db)


@router.get("/", response_model=list[temp_schemas.TemperatureResponse])
async def get_temperatures(
    db: AsyncSession = Depends(get_db),
    city_id: int = Query(default=None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    temperatures = await temp_crud.get_temperatures(
        db=db, skip=skip, limit=limit, city_id=city_id
    )

    return [
        temp_schemas.TemperatureResponse.model_validate(temp) for temp in temperatures
    ]
