from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.cities_rep import CityRep, get_city_rep
from schemas.cities_schema import CityCreateSchema


cities_router = APIRouter()

city_rep = Annotated[CityRep, Depends(get_city_rep)]


@cities_router.post(
    path="/cities/",
    description="Create a new city.",
    status_code=201
)
async def create_city(
        rep: city_rep,
        city_data: CityCreateSchema,
):
    return await rep.add_city(city_data)


@cities_router.get(
    path="/cities/",
    description="Get a list of all cities."
)
async def get_cities(
        rep: city_rep,
):
    return await rep.get_cities()


@cities_router.get(
    path="/cities/{city_id}/",
    description="Get the details of a specific city."
)
async def get_city(
        rep: city_rep,
        city_id: int
):
    return await rep.get_city(city_id)


@cities_router.put(
    path="/cities/{city_id}/",
    description="Update the details of a specific city."
)
async def update_city(
        rep: city_rep,
        city_id: int,
        city_data: CityCreateSchema
):
    return await rep.update_city(city_id, city_data)


@cities_router.delete(
    path="/cities/{city_id}/",
    description="Delete a specific city."
)
async def delete_city(
        rep: city_rep,
        city_id: int
):
    return await rep.remove_city(city_id)
