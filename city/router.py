from fastapi import APIRouter, Depends, HTTPException
from dependencies import CommonDB, CommonLimitation
from city.dependencies import CommonParametersWithId
import schemas
import crud

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: CommonDB) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(common: CommonLimitation, db: CommonDB) -> list[schemas.City]:
    cities = await crud.get_cities(db, skip=common["skip"], limit=common["limit"])
    return cities


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_city(city_id: CommonParametersWithId, db: CommonDB) -> schemas.City:
    db_city = await crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city(city_id: CommonParametersWithId, db: CommonDB) -> schemas.City:
    db_city = await crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    await crud.delete_city(db, city_id=city_id)
    return db_city
