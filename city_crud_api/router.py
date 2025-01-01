from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city_crud_api import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=schemas.CityList)
async def get_cities(db: AsyncSession = Depends(get_db)):
    try:
        cities = await crud.get_all_cities(db=db)
        if not cities:
            raise HTTPException(status_code=404, detail="No cities found.")
        return {"cities": cities}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch cities.")


@router.get("/cities/{city_id}", response_model=schemas.CityRead)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    try:
        city = await crud.get_city_by_id(db=db, city_id=city_id)
        if not city:
            raise HTTPException(status_code=404, detail="City not found.")
        return schemas.CityRead.from_orm(city)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch the city.")


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_city(db=db, city=city)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create the city.")


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(city_id: int, city: schemas.CityUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.update_city(city_id=city_id, city=city, db=db)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update the city.")


@router.delete("/cities/{city_id}", status_code=204)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await crud.delete_city(city_id=city_id, db=db)
        return {"detail": "City successfully deleted."}
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete the city.")
