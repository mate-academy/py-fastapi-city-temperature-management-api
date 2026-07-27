from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from temperature_api import temp_schemas, temp_crud
from city_api import city_crud

import weather_api


router = APIRouter()


@router.post("/temperatures/update")
async def create_temperature(
    db: Session = Depends(get_db)
):
    city_list = city_crud.get_city_list(db=db)
    return await weather_api.create_temperature_from_list(db=db, city_list=city_list)


@router.get("/temperatures/", response_model=list[temp_schemas.Temperature])
def get_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db)
):
    if city_id is None:
        return temp_crud.get_temperatures_list(db=db)

    db_temp = temp_crud.get_temperatures_by_city_id(db=db, city_id=city_id)

    if db_temp is None:
        raise HTTPException(
            status_code=404,
            detail=f"Historian data for {city_id} is not found!"
        )
    return db_temp