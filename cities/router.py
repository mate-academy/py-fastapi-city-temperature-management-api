from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import dependencies
from cities import schemas, crud

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(dependencies.get_db)
):
    db_city = crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400,
            detail="Such name for City already exists"
        )

    return crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(
        db: Session = Depends(dependencies.get_db),
):
    return crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def retrieve_city(
        city_id: int,
        db: Session = Depends(dependencies.get_db)
):
    db_city = crud.retrieve_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(
            status_code=400,
            detail="Such id is not found"
        )

    return db_city


@router.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(dependencies.get_db)):
    db_city = crud.retrieve_city(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(
            status_code=400,
            detail="Such id for City is not found"
        )

    db.delete(db_city)
    db.commit()

    return {"ok": True}


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: Session = Depends(dependencies.get_db)
):
    updated_city = crud.retrieve_city(db=db, city_id=city_id)

    if updated_city is None:
        raise HTTPException(
            status_code=400,
            detail="City not found"
        )

    if city.name:
        updated_city.name = city.name

    if city.additional_info and city.additional_info != "string":
        updated_city.additional_info = city.additional_info

    db.commit()
    db.refresh(updated_city)

    return updated_city
