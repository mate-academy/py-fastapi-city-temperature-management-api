from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.exeptions import CityNotFound, CityAlreadyExist
from app.schemes.city import (
    CityCreate, CityUpdate, CityResponse
)
from app.db.database import get_db
from app.db import crud

router = APIRouter(
    prefix="/cities",
    tags=["City"]
)


@router.get("/", response_model=list[CityResponse])
def get_cities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> list[CityResponse]:
    return crud.get_all_cities(db, skip=skip, limit=limit)


@router.get("/id/{city_id}", response_model=CityResponse)
def get_city_by_id(
    city_id: int,
    db: Session = Depends(get_db)
) -> CityResponse:
    try:
        return crud.get_city_by_id(db, city_id)
    except CityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/name/{city_name}", response_model=CityResponse)
def get_city_by_name(
    city_name: str,
    db: Session = Depends(get_db)
) -> CityResponse:
    try:
        return crud.get_city_by_name(db, city_name)
    except CityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=CityResponse)
def create_new_city(
        data: CityCreate,
        db: Session = Depends(get_db)) -> CityResponse:
    try:
        return crud.create_city(db, data)
    except CityAlreadyExist as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{city_id}", response_model=CityResponse)
def update_city(
        city_id: int,
        data: CityUpdate,
        db: Session = Depends(get_db)
) -> CityResponse:
    try:
        return crud.update_city(db, city_id, data)
    except CityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{city_id}", status_code=204)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> None:
    try:
        crud.delete_city(db, city_id)
    except CityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))