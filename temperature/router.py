from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from . import crud
from . import schemas
from city.dependencies import get_db

router = APIRouter()


@router.post("/temperatures/update/", status_code=status.HTTP_200_OK)
def update_temperatures(db: Session = Depends(get_db)):
    crud.update_temperatures(db=db)


@router.get("/temperatures/", response_model=list[schemas.Temperature] | schemas.Temperature)
def get_temperatures(db: Session = Depends(get_db), city_id: int = None):
    if city_id is not None:
        return crud.get_temperature_by_city_id(db=db, city_id=city_id)
    return crud.get_all_temperatures(db=db)
