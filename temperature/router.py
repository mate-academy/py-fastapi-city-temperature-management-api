from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from temperature.crud import update_temperature_for_cities, get_list_of_all_temperature_records, \
    get_temperature_by_city_id
from dependencies import get_db, common_parameters
from temperature.schemas import Temperature, OnlineResponse

router = APIRouter()
CommonDeps = Annotated[dict, Depends(common_parameters)]

@router.post("/temperature/updates", response_model=OnlineResponse, tags=["Temperature CRUD"])
async def update_all_temperature_for_cities(db: Session = Depends(get_db)):
    result = await update_temperature_for_cities(db)
    return result

@router.get("/temperatures", response_model=list[Temperature] , tags=["Temperature CRUD"])
async def get_all_temperature(commons: CommonDeps):
    return get_list_of_all_temperature_records(commons["db"], commons["skip"], commons["limit"])

@router.get("/temperature/{city_id}", response_model=list[Temperature], tags=["Temperature CRUD"])
async def get_all_temperature_by_city_id(city_id: int, db: Session = Depends(get_db)):
    return get_temperature_by_city_id(db, city_id)