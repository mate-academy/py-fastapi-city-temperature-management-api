import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from temperature import schemas, crud
from dependencies import get_db


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(db: Session = Depends(get_db)):
    return crud.get_temperatures(db=db)


@router.get("/temperatures/{city_id}", response_model=list[schemas.Temperature])
def read_temperatures(city_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/update/")
def update_temperatures(db: Session = Depends(get_db)):
    try:
        asyncio.run(crud.set_temps(db=db))
    except Exception as e:
        return {"Error": e.__str__()}
    else:
        return {"ok": True}
