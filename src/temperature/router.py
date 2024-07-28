from typing import List, Dict, Annotated

from fastapi import APIRouter, Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.temperature import schemas, crud
from src.temperature.utils import get_async_client, fetch_temperature
from src.database import get_async_session

router = APIRouter()


async def paginate_parameters(
        offset: int = 0, limit: int = 100
) -> dict:
    return {"offset": offset, "limit": limit}


PaginateDep = Annotated[dict, Depends(paginate_parameters)]


@router.get("/temperatures/update/")
async def fetch_temperatures(
    client: AsyncClient() = Depends(get_async_client),
    session: AsyncSession = Depends(get_async_session),
) -> Dict[str, str]:
    return await fetch_temperature(session=session, client=client)


@router.get("/temperatures/", response_model=List[schemas.Temperature])
async def get_temperatures(
    city_id: int,
    paginate_params: PaginateDep,
    session: AsyncSession = Depends(get_async_session),

) -> List[schemas.Temperature]:
    return await crud.get_temperature(
        session=session,
        city_id=city_id,
        **paginate_params
    )
