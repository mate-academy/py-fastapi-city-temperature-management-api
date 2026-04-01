from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from tools.tools import DataBase
from routers.cities import CityDoesntExistError
from db import crud
from db.schemas import TemperatureRelDTO

temperatures_router = APIRouter()

@temperatures_router.post("/temperatures/update", status_code=status.HTTP_201_CREATED)
async def fetch_all_temperatures(
    db: DataBase,
):
    cities = await crud.select_all_cities(db=db)
    try:
        await crud.fetch_and_store_all_temperatures(db=db, cities=cities)
    except KeyError:
        raise HTTPException(status_code=401, detail="Unauthorized API key")
    return


@temperatures_router.get("/temperatures", response_model=list[TemperatureRelDTO])
async def get_temperatures(
    db: DataBase,
    city_id: int | None = None
):
    if city_id:
        city = await crud.select_city_by_id(db=db, city_id=city_id)
        if not city:
            raise CityDoesntExistError

        return await crud.select_temperature_by_city_id(db=db, city_id=city_id)
    else:
        temperatures = await crud.select_all_temperatures(db=db)
        return temperatures
