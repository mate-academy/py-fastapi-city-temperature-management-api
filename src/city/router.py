from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.city import schemas, crud
from src.database import get_async_session

router = APIRouter()


async def paginate_parameters(offset: int = 0, limit: int = 100) -> dict:
    return {"offset": offset, "limit": limit}


@router.get("/cities/", response_model=List[schemas.City])
async def get_cities(
    paginate_params: Annotated[dict, Depends(paginate_parameters)],
    session: AsyncSession = Depends(get_async_session),
) -> List[schemas.City]:
    return await crud.get_cities(session=session, **paginate_params)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.create_city(session=session, city=city)


@router.get("/cities/{id}/", response_model=schemas.City)
async def retrieve_city(
    id: int,
    session: AsyncSession = Depends(get_async_session),
) -> schemas.City:
    return await crud.retrieve_city(
        session=session,
        id=id,
    )


@router.put("/cities/{id}/", response_model=schemas.City)
async def update_city(
    id: int,
    city: schemas.CityBase,
    session: AsyncSession = Depends(get_async_session),
) -> schemas.City:
    return await crud.update_city(session=session, id=id, city=city)


@router.delete("/cities/{id}/", response_model=schemas.City)
async def update_city(
    id: int,
    session: AsyncSession = Depends(get_async_session),
) -> schemas.City:
    return await crud.delete_city(
        session=session,
        id=id,
    )
