from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from cities import schemas, models, crud
from dependencies import get_db
from temperature import crud as temperature_crud


router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
) -> models.City:
    db_city = crud.create_city(db=db, city=city)
    await temperature_crud.create_city_temperature(
        db,
        db_city,
        background_tasks
    )
    return db_city


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> list[schemas.City]:
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@router.get("/cities/{city_id}", response_model=schemas.City)
def read_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> schemas.City:
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
        city_id: int,
        city: schemas.CityBase,
        db: Session = Depends(get_db)
) -> models.City | None:
    updated_city = crud.update_city(
        city_id=city_id,
        city=city,
        db=db
    )
    if updated_city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return updated_city


@router.delete("/cities/{city_id}")
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> dict:
    deleted_city = crud.delete_city(
        city_id=city_id,
        db=db
    )
    if deleted_city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return {"message": "City deleted successfully"}
