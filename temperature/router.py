from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from . import crud, schemas


router = APIRouter()


@router.post("/temperatures/update/")
def update_temperatures(db: Session = Depends(get_db)):
    crud.update_all_temperatures(db=db)
    return {"message": "Temperatures updated"}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_temperatures(db=db, city_id=city_id)
