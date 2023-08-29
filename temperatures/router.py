from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

import temperatures.crud as crud
import temperatures.schemas as schemas
from cities.crud import get_city_by_id
from dependencies import get_db, pagination_param

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(
    pagination: Annotated[dict, Depends(pagination_param)],
    db: Session = Depends(get_db),
    city_id: int = Query(None, description="City id"),
):
    db_city = get_city_by_id(db=db, city_id=city_id)

    if city_id and not db_city:
        raise HTTPException(status_code=404, detail="Such city not found")

    return crud.read_all_temperatures(db=db, city_id=city_id, **pagination)


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
def update_temperatures(db: Session = Depends(get_db)):
    return crud.update_all_city_temperatures(db=db)
