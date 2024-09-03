from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import asyncio

from app import crud, schemas, models
from app.dependencies import get_db

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[schemas.Temperature]:
    return await crud.get_temperatures(db=db, skip=skip, limit=limit)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures_by_city(city_id: int, db: Session = Depends(get_db)) -> list[schemas.Temperature]:
    db_temperatures = crud.get_temperatures_by_city(db=db, city_id=city_id)
    if not db_temperatures:
        raise HTTPException(status_code=404, detail="No temperature records found for the city")
    return await db_temperatures


@router.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)) -> dict[str, str]:
    await crud.update_city_temperatures(db=db)
    return await {"detail": "Temperatures updated"}
