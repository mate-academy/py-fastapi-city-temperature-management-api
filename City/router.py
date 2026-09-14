from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from City import schemas, crud
from database import SessionLocal

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/cities/", response_model=list[schemas.City])
def get_city(db: Session = Depends(get_db)) -> list[schemas.City]:
    return crud.get_all_city(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
def get_city_by_id(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city_by_id(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    return city


@router.post("/cities/", response_model=schemas.City)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
):
    db_city_name = crud.get_city_by_name(db=db, name=city.name)

    if db_city_name:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists",
        )
    return crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
        city: schemas.CityUpdate,
        city_id: int,
        db: Session = Depends(get_db),
):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail="Such a city does not exist",
        )

    return crud.update_city(db=db, city=city, db_city=db_city)


@router.delete("/cities/{city_id}", response_model=schemas.City)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db),
):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail="Such a city does not exist",
        )

    return crud.delete_city(db=db, db_city=db_city)
