from fastapi import APIRouter, HTTPException, status

from app.schemas import city as city_schema
from app.dependencies import CurrentSession
from app.services import city_service

router = APIRouter(prefix="/cities", tags=["cities"])

@router.get("/", response_model=list[city_schema.City])
def get_cities(
        db: CurrentSession
) -> list[city_schema.City]:
    return city_service.get_cities(db)

@router.post("/", response_model=city_schema.City)
def create_city(
        db: CurrentSession,
        city: city_schema.CityCreate
) -> city_schema.City:
    return city_service.create_city(db, city)

@router.get("/{city_id}/", response_model=city_schema.City)
def get_city(
        db: CurrentSession,
        city_id: int
) -> city_schema.City:
    city = city_service.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.put("/{city_id}/", response_model=city_schema.City)
def update_city(
        db: CurrentSession,
        city_id: int,
        city: city_schema.CityCreate
) -> city_schema.City:
    updated_city = city_service.update_city(db, city_id, city)
    if not updated_city:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city

@router.delete("/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(
        db: CurrentSession,
        city_id: int
) -> None:
    deleted_city = city_service.delete_city(db, city_id)
    if not deleted_city:
        raise HTTPException(status_code=404, detail="City not found")
    return None
