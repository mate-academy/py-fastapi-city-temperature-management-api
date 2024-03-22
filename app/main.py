from fastapi import Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas, database
from app.api import router


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(router)


# Dependency
def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/cities/', response_model=schemas.City)
def create_city(city: schemas.CityCreate,
                db: Session = Depends(get_db)) -> schemas.City:
    return crud.create_city(db=db, city=city)


@app.get('/cities/', response_model=List[schemas.City])
def read_cities(skip: int = 0,
                limit: int = 100,
                db: Session = Depends(get_db)) -> List[schemas.City]:
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@app.get('/cities/{city_id}', response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)) -> schemas.City:
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail='City not found')
    return db_city


@app.delete('/cities/{city_id}', response_model=schemas.City)
def delete_city(city_id: int,
                db: Session = Depends(get_db)) -> dict:
    deleted = crud.delete_city(db, city_id=city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='City not found')
    return {'detail': 'City deleted'}
