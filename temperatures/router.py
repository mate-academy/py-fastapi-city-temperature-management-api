from asyncio import TaskGroup

from fastapi import APIRouter, status
from httpx import AsyncClient

from cities import crud as cities_crud
from dependencies import SessionDep, PaginationHelper
from temperatures import crud
from temperatures.models import Temperature
from temperatures.schemas import Temperature
from temperatures.services import fetch_data

router = APIRouter(
    prefix="/temperatures",
)


@router.post(
    "/update",
    response_model=list[Temperature],
    status_code=status.HTTP_201_CREATED,
    responses={502: {"description": "Weather api server problem"}},
)
async def update_cities(db: SessionDep):
    cities = await cities_crud.all_cities_list(db=db)

    async with AsyncClient() as async_client:
        async with TaskGroup() as tg:
            results = [
                tg.create_task(fetch_data(client=async_client, city=city))
                for city in cities
            ]

    result = [Temperature(**task.result().model_dump()) for task in results]

    return await crud.create_all_cities_temperature(db=db, temperatures=result)


@router.get("/", response_model=list[Temperature])
async def read_cities(
    db: SessionDep, pagination: PaginationHelper, city_id: int | None = None
):
    return await crud.all_temperature(
        db=db, limit=pagination.limit, skip=pagination.skip, city_id=city_id
    )
