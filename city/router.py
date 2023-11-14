from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
def create_cities(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_cities(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_single_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
    city_id: int, city: schemas.City, db: Session = Depends(get_db)
):
    city_to_update = crud.get_city(db, city_id)

    if not city_to_update:
        raise HTTPException(status_code=404, detail="City not found")

    updated_city = crud.update_city(db, city_to_update, city)
    return updated_city


@router.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city_to_delete = crud.delete_city(db=db, city_id=city_id)

    if not city_to_delete:
        raise HTTPException(status_code=404, detail="City not found")
    return {"Success": "City has been removed"}
