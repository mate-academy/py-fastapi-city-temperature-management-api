from fastapi import APIRouter, HTTPException, status

from cities import crud
from cities.schemas import City, CityCreate
from dependencies import SessionDep, PaginationHelper

router = APIRouter(
    prefix="/cities",
)


@router.get("/", response_model=list[City])
async def get_all_cities(db: SessionDep, pagination: PaginationHelper):
    return await crud.all_cities_list_with_pagination(
        db=db, skip=pagination.skip, limit=pagination.limit
    )


@router.post("/", response_model=City, status_code=status.HTTP_201_CREATED)
async def create_city(db: SessionDep, city: CityCreate):
    return await crud.create_city(db=db, city_data=city)


@router.get(
    "/{city_id}", response_model=City, responses={404: {"description": "Not found"}}
)
async def get_city(db: SessionDep, city_id: int):
    city = await crud.city_by_id(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City was not found")

    return city


@router.put(
    "/{city_id}", response_model=City, responses={404: {"description": "Not found"}}
)
async def completely_update_city(db: SessionDep, city_id: int, city_data: CityCreate):
    city = await crud.city_by_id(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City was not found")

    return await crud.completely_update_city(db=db, city=city, city_data=city_data)


@router.delete(
    "/{city_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Not found"}},
)
async def delete_city(db: SessionDep, city_id: int):
    city = await crud.city_by_id(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City was not found")

    await crud.delete_city(db=db, city=city)
