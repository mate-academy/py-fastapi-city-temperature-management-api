from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from . import schemas, crud, models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/cities/", response_model=schemas.CityRead)
def create_city(city: schemas.CityCreateUpdate, db: Session = Depends(get_db)):
    db_city = crud.create_city(db=db, city=city)
    if db_city is None:
        raise HTTPException(status_code=400, detail="Values are invalid")
    return db_city


@router.get("/cities/", response_model=list[schemas.CityRead])
def read_cities(db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db)
    return cities


@router.get("/cities/{city_id}/", response_model=schemas.CityRead)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.CityRead)
def update_city(city_id: int, city: schemas.CityCreateUpdate, db: Session = Depends(get_db)):
    db_city = crud.update_city(db=db, city_id=city_id, updated_city=city)
    if db_city is None:
        raise HTTPException(status_code=400, detail="Values are invalid")
    return db_city


@router.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    crud.delete_city(db=db, city_id=city_id)


@router.put("/temperatures/update/")
async def update_cities_temperature(db: Session = Depends(get_db)):
    return await crud.update_temperatures(db=db)


@router.get("/temperatures/", response_model=list[schemas.TemperatureRead])
def get_temperatures(city_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db=db, city_id=city_id)
