from ast import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.dependencies import DB

from app import crud, schemas, models

router = APIRouter()

@router.get("/cities/", response_model=List[schemas.City])
async def read_cities(db: DB):
    return crud.get_all_cities(db)


@router.post("/cities/", response_model=schemas.City)
async def create_cities(
        city: schemas.CityCreate,
        db: DB
):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: DB):
    db_city = crud.get_city_by_id(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city():
    pass


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: DB):
    db_city = db.query(models.CityDB).filter(models.CityDB.id == city_id).first()

    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Місто з таким ID не знайдено"
        )

    db.delete(db_city)
    db.commit()
    return None