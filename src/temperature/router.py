from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .schemas import Temperature
from src.dependencies import get_db, common_parameters
from . import crud


router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.get("/", response_model=list[Temperature])
def read_temperature_list(
        parameters: Annotated[dict, Depends(common_parameters)],
        db: Session = Depends(get_db)
) -> list[Temperature]:
    return crud.get_temperature_list(db=db, **parameters)


@router.get("/{city_id}/", response_model=Temperature)
def rear_temperature_by_city_id(
        city_id: int,
        db: Session = Depends(get_db),
):
    return crud.get_temperature_for_a_city(db, city_id)


@router.post("/update/", response_model=list[Temperature])
async def update_temperature(
        db: Session = Depends(get_db)
):
    return await crud.update_cities_temperature(db=db)
