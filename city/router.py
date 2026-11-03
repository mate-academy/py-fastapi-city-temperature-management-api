from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND

from city import schemas, crud
from dependencies import get_db

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get("/", response_model=list[schemas.CityRead])
def read_city(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.post("/", response_model=schemas.CityRead, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exist"
        )

    return crud.create_city(db=db, city=city)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    success = crud.delete_city(db, city_id=city_id)
    if not success:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    return None

