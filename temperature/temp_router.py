from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from temperature import schemas, crud

router = APIRouter(
    tags=["Temperatures"],
    prefix="/temperatures"
)


@router.get("/", response_model=List[schemas.Temperature])
async def get_all_temperatures(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    temperatures = await crud.get_all_temperature(db=db, skip=skip, limit=limit)
    return temperatures


@router.get("/{temperature_id}", response_model=schemas.Temperature)
async def get_temperature_by_id(temperature_id: int, db: Session = Depends(get_db)):
    temperature = await crud.get_temperature_by_id(db=db, temperature_id=temperature_id)
    if temperature is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Temperature not found")
    return temperature


@router.post("/", response_model=schemas.Temperature, status_code=status.HTTP_201_CREATED)
async def create_temperature(temperature: schemas.TemperatureCreate, db: Session = Depends(get_db)):
    return await crud.create_temperature(db=db, temperature=temperature)



@router.put("/{temperature_id}", response_model=schemas.Temperature)
async def update_temperature(temperature_id: int, temperature: schemas.TemperatureUpdate, db: Session = Depends(get_db)):
    updated_temperature = await crud.update_temperature(db=db, temperature_id=temperature_id, temperature=temperature)
    if updated_temperature is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Temperature not found")
    return updated_temperature


@router.delete("/{temperature_id}", response_model=schemas.Temperature, status_code=status.HTTP_204_NO_CONTENT)
async def delete_temperature(temperature_id: int, db: Session = Depends(get_db)):
    deleted_temperature = await crud.delete_temperature(db=db, temperature_id=temperature_id)
    if deleted_temperature is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Temperature not found")
    return deleted_temperature
