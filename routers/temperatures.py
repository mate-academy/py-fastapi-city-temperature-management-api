from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query

from repositories.temps_rep import TempRepository, get_rep
from schemas.temps_schema import TempListSchema

temps_router = APIRouter()
temp_tep_dep = Annotated[TempRepository, Depends(get_rep)]


@temps_router.get(
    path="/temperatures/",
    description="Get the temperature records for a specific city.",
    response_model=TempListSchema
)
async def get_temps_by_city(
        temp_rep: temp_tep_dep,
        city_id: Annotated[Optional[int], Query()] = None,
) -> TempListSchema:
    return await temp_rep.get_temps_by_city(city_id)


@temps_router.post(
    path="/temperatures/update/",
    description="fetches the current temperature for "
                "all cities in the database from an online resource of your choice."
                "Store this data in the Temperature table. "
                "You should use an async function to fetch the temperature data."
)
async def update_temps(
        temp_rep: temp_tep_dep
) -> dict:
    await temp_rep.update_temps_for_all_cities()
    return {"detail": "All Cities updated successfully!"}
