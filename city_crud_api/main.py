from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from city_crud_api.db.engine import get_db
from city_crud_api.api import crud, schemas

app = FastAPI()


@app.post("/cities/", response_model=schemas.CityCreate, status_code=201)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_new_city(db=db, city_data=city)


@app.get("/cities/", status_code=200)
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)
