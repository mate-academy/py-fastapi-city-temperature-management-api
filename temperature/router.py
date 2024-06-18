from fastapi import APIRouter, Depends
from dependencies import CommonDB, CommonLimitation
import schemas
import crud

router = APIRouter()


@router.post("/temperatures/", response_model=schemas.Temperature)
async def create_temperature(temperature: schemas.TemperatureCreate, db: CommonDB) -> schemas.Temperature:
    return await crud.create_temperature(db=db, temperature=temperature)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(common: CommonLimitation, db: CommonDB) -> list[schemas.Temperature]:
    temperatures = await crud.get_temperatures(db, skip=common["skip"], limit=common["limit"])
    return temperatures


@router.get("/temperatures/{city_id}/", response_model=list[schemas.Temperature])
async def read_temperatures_by_city(city_id: int, common: CommonLimitation, db: CommonDB) -> list[schemas.Temperature]:
    temperatures = await crud.get_temperatures_by_city(db, city_id=city_id, skip=common["skip"], limit=common["limit"])
    return temperatures
