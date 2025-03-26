from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from temperature import crud, schemas
from utils import get_db

router = APIRouter()


@router.post("/update/")
def temperatures_update(db: Session = Depends(get_db)):
    return crud.temperature_update(db=db)


@router.get("/", response_model=list[schemas.Temperature])
def get_temperature_list(
        city_id: int | None = None,
        db: Session = Depends(get_db)
):
    return crud.get_temperatures(db=db, city_id=city_id)
