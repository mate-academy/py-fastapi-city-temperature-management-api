from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from . import crud
from . import schemas
from database import SessionLocal
from . import service

router = APIRouter()

def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)

@router.post("/cities/", response_model=schemas.City)
def create_new_city(city: schemas.CreateCity, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)

@router.get("/cities/{city_id}", response_model=schemas.CityDetail)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city_id(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )
    return city

@router.put("/cities/{city_id}", response_model=schemas.CityDetail)
def update_city(city_id: int, city: schemas.UpdateCity, db: Session = Depends(get_db)):
    return crud.update_city(db=db, city_id=city_id, city=city)

@router.delete("/cities/{city_id}", response_model=schemas.CityDetail)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    return crud.delete_city(db=db, city_id=city_id)

@router.get("/temperatures/")
async def get_temperatures(
        city_id: int | None=None,
        db: Session = Depends(get_db)
):
    return crud.get_temperatures(db=db, city_id=city_id)

@router.post("/temperatures/update/")
async def update_temperature(db: Session = Depends(get_db)):

    cities = crud.get_all_cities(db)

    if not cities:
        raise HTTPException(
            status_code=404,
            detail="No cities found."
        )

    for city in cities:
        try:
            temperature = await service.get_temperature(city.name)

            crud.create_temperature(db=db, city_id=city.id, temperature=temperature)

        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to get temperature for city '{city.name}': {str(e)}"
            )

    return {"message": "Temperatures updated successfully"}
