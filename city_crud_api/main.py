from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from city_crud_api.api.crud import retrieve_specific_city, update_specific_city
from city_crud_api.db.engine import get_db
from city_crud_api.api import crud, schemas

app = FastAPI()


@app.post("/cities/", response_model=schemas.CityCreate, status_code=201)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_new_city(db=db, city_data=city)


@app.get("/cities/", status_code=200)
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)

@app.get("/cities/{city_id}", status_code=200)
def retrieve_city(city_id: int, db: Session = Depends(get_db)):

    city = retrieve_specific_city(city_id=city_id, db=db)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@app.put("/cities/{city_id}", status_code=200, response_model=schemas.CityCreate,)
def edit_city( city: schemas.CityCreate, city_id: int, db: Session = Depends(get_db)):
    city = crud.update_specific_city(
        db=db,
        city_id=city_id,
        city_data=city,
    )

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    return city

@app.delete("/cities/{city_id}", status_code=200)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.delete_specific_city(
        db=db,
        city_id=city_id,
    )

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    return city
