from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from cities import schemas, crud
from database import get_db

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post(
    "/",
    response_model=schemas.City,
    status_code=status.HTTP_201_CREATED,
)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, city.name)
    if db_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City already exists"
        )
    return crud.create_city(db=db, city=city)


@router.get("/", response_model=list[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    return db_city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
        city_id: int,
        city_update: schemas.CityUpdate,
        db: Session = Depends(get_db),
):
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    if city_update.name and city_update.name != db_city.name:
        existing_city = crud.get_city_by_name(db, name=city_update.name)
        if existing_city:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="City with this name already exists",
            )

    return crud.update_city(db=db, db_city=db_city, city_update=city_update)


@router.delete("/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return crud.delete_city(db=db, db_city=db_city)