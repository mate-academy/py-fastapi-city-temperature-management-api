from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

import city.schemas as schemas
import city.crud as crud
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=schemas.CityResponse, status_code=201)
async def create_city(
    data: schemas.CityCreateRequest, db: AsyncSession = Depends(get_db)
) -> schemas.CityResponse:
    try:
        city = await crud.create_new_city(db, data.name, data.additional_info)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(detail=str(e), status_code=500)

    return schemas.CityResponse.model_validate(city)


@router.get("/cities/", response_model=schemas.CityListResponse)
async def get_cities(db: AsyncSession = Depends(get_db)) -> schemas.CityListResponse:
    cities = await crud.get_cities(db)
    return schemas.CityListResponse(cities=cities)


@router.get("/cities/{city_id}/", response_model=schemas.CityResponse)
async def get_city(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.CityResponse:
    city = await crud.get_city(db, city_id)
    if not city:
        raise HTTPException(detail="City not found", status_code=404)
    return schemas.CityResponse.model_validate(city)


@router.put("/cities/{city_id}/", response_model=schemas.CityResponse)
async def put_city(
    city_id: int, data: schemas.CityCreateRequest, db: AsyncSession = Depends(get_db)
) -> schemas.CityResponse:
    try:
        city = await crud.update_city(db, city_id, data.name, data.additional_info)
        if city is None:
            raise HTTPException(status_code=404, detail="City not found")
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(detail=str(e), status_code=500)
    return schemas.CityResponse.model_validate(city)


@router.delete("/cities/{city_id}/")
async def delete_city(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.MessageResponse:
    try:
        await crud.delete_city(db, city_id)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(detail=str(e), status_code=500)
    return schemas.MessageResponse(msg="City deleted successfully!")
