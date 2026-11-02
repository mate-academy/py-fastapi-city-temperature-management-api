from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from cities import schemas, crud
from database import get_db_session

app = FastAPI()


@app.post("/cities/", response_model=schemas.ReadCitySchema)
def create_city(
        city: schemas.CreateCitySchema,
        db_session: Annotated[Session, Depends(get_db_session)]
):
    return crud.create_city(db_session=db_session, city=city)


@app.get("/cities/", response_model=list[schemas.ReadCitySchema])
def read_cities(
        db_session: Annotated[Session, Depends(get_db_session)]
):
    return crud.get_cities(db_session=db_session)


@app.get("/cities/{city_id}/", response_model=schemas.ReadCitySchema)
def read_city(
        city_id: int,
        db_session: Annotated[Session, Depends(get_db_session)]
):
    city_from_db = crud.get_city_by_id(db_session=db_session, city_id=city_id)
    if city_from_db is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city_from_db


@app.delete("/cities/{city_id}/", status_code=204)
def delete_city(
        db_session: Annotated[Session, Depends(get_db_session)],
        city_id: int
):
    if not crud.delete_city(db_session=db_session, city_id=city_id):
        raise HTTPException(status_code=404, detail="City not found")
