from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from city import crud
from city.schemas import City, CityCreate

router = APIRouter()


@router.get("/city/", response_model=list[City])
def read_city(db: Session = Depends(get_db)):
    return crud.get_all_city(db=db)


@router.post("/city", response_model=City)
def create_city(
    city: CityCreate,
    db: Session = Depends(get_db)
):
    db_city = crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400,
            detail="Such name for City already exists"
        )
    return crud.create_city(db=db, city=city)


@router.get("/city/{city_id}/", response_model=City)
def read_single_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.delete("/city/{city_id}/", response_model=City)
def delete_single_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(db_city)
    db.commit()
    return db_city


@router.put("/city/{city_id}/", response_model=City)
def update_single_city(city_id: int, city: CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    for attr, value in city.dict().items():
        setattr(db_city, attr, value)

    db.commit()
    db.refresh(db_city)
    return db_city
