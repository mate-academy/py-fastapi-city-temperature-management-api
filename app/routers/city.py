from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from app.schemas.city import CityRead
from app.repositories import CityRepository
from app.dependencies import get_city_repository
from app.schemas.city import CityCreate, CityUpdate

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=CityRead, status_code=status.HTTP_201_CREATED)
def create_city(
        city: CityCreate,
        repo: CityRepository = Depends(get_city_repository)
):
    existing_city = repo.get_by_name(city.name)
    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"City with name '{city.name}' already exists"
        )

    return repo.create(city)


@router.get("/", response_model=list[CityRead])
def get_cities(
        skip: int = 0,
        limit: int = 100,
        repo: CityRepository = Depends(get_city_repository)
):
    cities = repo.get_all(skip=skip, limit=limit)
    return cities


@router.get("/{city_id}", response_model=CityRead)
def get_city(
        city_id: int,
        repo: CityRepository = Depends(get_city_repository)
):
    city = repo.get_by_id(city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found"
        )
    return city


@router.put("/{city_id}", response_model=CityRead)
def update_city(
        city_id: int,
        city_update: CityUpdate,
        repo: CityRepository = Depends(get_city_repository)
):
    if city_update.name:
        existing_city = repo.get_by_name(city_update.name)
        if existing_city and existing_city.id != city_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"City with name '{city_update.name}' already exists"
            )

    updated_city = repo.update(city_id, city_update)
    if not updated_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found"
        )

    return updated_city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(
        city_id: int,
        repo: CityRepository = Depends(get_city_repository)
):
    success = repo.delete(city_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found"
        )
    return None
