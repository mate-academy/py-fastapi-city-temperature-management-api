from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from temperature import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def list_temperatures(
    city_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_all_temperatures(
        skip=skip, limit=limit, db=db, city_id=city_id
    )
