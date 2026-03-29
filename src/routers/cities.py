from fastapi import APIRouter, HTTPException
from starlette import status

from src.dependencies import DBSessionDep
from src.services import city_service

from src.schemas.city import CityRead, CityCreate, CityUpdate

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=CityRead)
async def create_city(payload: CityCreate, db: DBSessionDep):
    city = await city_service.create_city(db=db, payload=payload)
    return city


@router.get("/", response_model=list[CityRead])
async def get_cities(db: DBSessionDep):
    cities = await city_service.get_cities(db=db)
    return cities


@router.get("/{city_id}", response_model=CityRead)
async def get_city(city_id, db: DBSessionDep):
    city = await city_service.get_city_by_id(city_id=city_id, db=db)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return city


@router.put("/{city_id}", response_model=CityRead)
async def update_city(city_id, payload: CityUpdate, db: DBSessionDep):
    updated_city = await city_service.update_city(city_id, db=db, payload=payload)
    if not updated_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return updated_city


@router.delete("/{city_id}", status_code=status.HTTP_200_OK)
async def delete_city(city_id, db: DBSessionDep):
    success = await city_service.delete_city(city_id=city_id, db=db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return {"status": "success", "message": f"City was successfully deleted"}
