from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
async def get_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[schemas.City] :
    return await crud.get_cities(db=db, skip=skip, limit=limit)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def get_city(city_id: int, db: Session = Depends(get_db)) -> schemas.City:
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return await db_city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(city_id: int, city_update: schemas.CityUpdate, db: Session = Depends(get_db)) -> schemas.City:
    db_city = crud.update_city(db=db, city_id=city_id, city_update=city_update)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return await db_city


@router.delete("/cities/{city_id}")
async def delete_city(city_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    crud.delete_city(db=db, city_id=city_id)
    return await {"detail": "City deleted"}
