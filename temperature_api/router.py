from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from dependencies import get_db
from temperature_api import schemas, crud

router = APIRouter()



@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures_list(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_temperature(db=db)


@router.post("/temperatures/", response_model=schemas.Temperature)
async def create_temperature(
        temperature: schemas.TemperatureCreate,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    db_temperature = await crud.get_temperature_by_id(db=db, temperature_id=temperature.id)

    if db_temperature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This temperature already exists.",
        )

    try:
        return await crud.create_temperature(db=db, temperature=temperature)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch("/temperatures/{temperature_id}/", response_model=schemas.Temperature)
async def update_temperature(
        temperature_id: int,
        temperature_update: schemas.TemperatureUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    db_temperature = await crud.get_temperature_by_id(db=db, temperature_id=temperature_id)
    if db_temperature is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This temperature does not exist."
        )

    try:
        return await crud.update_temperature(db=db, db_temperature=db_temperature, temperature_update=temperature_update)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.delete("/temperatures/{temperature_id}/")
async def delete_temperature(
        db: Annotated[AsyncSession, Depends(get_db)],
        temperature_id: int,
):
    db_temperature = await crud.get_temperature_by_id(db=db, temperature_id=temperature_id)
    if db_temperature is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This temperature does not exist."
        )

    await crud.delete_temperature(db=db, db_temperature=db_temperature)


@router.post("/temperatures/update/", response_model=schemas.Temperature)
async def update_temperatures(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.update_all_temperatures(db=db)
