from fastapi import HTTPException, APIRouter

from app import schemas, crud
from app.dependencies import DBDep

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: DBDep):
    return await crud.get_cities_list(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(db: DBDep, city: schemas.CityCreate):
    db_city = await crud.get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already exists")

    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_single_city(db: DBDep, city_id: int):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
        db: DBDep,
        city_id: int,
        city: schemas.CityUpdate,
):
    db_city = await crud.update_city(db=db, city_id=city_id, city=city)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.delete("/cities/{city_id}")
async def delete_city(db: DBDep, city_id: int):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    await crud.delete_city(db=db, city_id=city_id)
    return {"deleted": True}
