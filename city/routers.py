from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from city import crud, schemas

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)) -> list[schemas.City]:
    return crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
def create_city(
    city_schema: schemas.CityCreateUpdate,
    db: Session = Depends(get_db)
) -> schemas.City:
    db_city = crud.get_city_by_name(db=db, city_name=city_schema.name)

    if db_city:
        raise HTTPException(
            status_code=400,
            detail=f"City with name {city_schema.name} already exists!"
        )

    return crud.create_city(db=db, city_schema=city_schema)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def retrieve_city(city_id: int, db: Session = Depends(get_db)) -> schemas.City:

    crud.city_exists(db=db, city_id=city_id)

    return crud.get_city_by_id(db=db, city_id=city_id)


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
    city_id: int,
    city_schema: schemas.CityCreateUpdate,
    db: Session = Depends(get_db)
) -> schemas.City:

    crud.city_exists(db=db, city_id=city_id)

    if crud.get_city_by_name(db=db, city_name=city_schema.name).id != city_id:
        raise HTTPException(
            status_code=400,
            detail=f"City with name {city_schema.name} already exists!"
        )

    return crud.update_city(db=db, city_id=city_id, city_schema=city_schema)


@router.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    crud.city_exists(db=db, city_id=city_id)
    return crud.delete_city(db=db, city_id=city_id)
