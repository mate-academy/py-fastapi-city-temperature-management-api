from typing import List, Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Query, HTTPException

from city import schemas, crud
from dependencies import get_db
from utils import general_parameter

router = APIRouter()


@router.get(
    "/cities/",
    response_model=List[schemas.CityList]
)
async def get_all_cities(
        general: Annotated[dict, Depends(general_parameter)]
) -> List[schemas.CityList]:
    return await crud.get_all_cities(**general)


@router.get(
    "/cities/{city_id}/",
    response_model=schemas.CityBase
)
async def get_single_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> schemas.CityBase:
    db_city = await crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return db_city


@router.post(
    "/cities/",
    response_model=schemas.CityList
)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db),
) -> schemas.CityList:
    db_city = await crud.get_city_by_name(
        db=db,
        name=city.name
    )
    is_not_city_name_exist = await crud.check_correct_city_name(name=city.name)

    if db_city or is_not_city_name_exist:
        raise HTTPException(
            status_code=400,
            detail="This name is already exist or incorrect name of city!"
        )

    return await crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}/")
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> dict:
    db_city = await crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    await crud.delete_city(db=db, city=db_city)
    return {"message": "City deleted successfully"}


@router.put("/cities/{city_id}/")
async def update_city(
        city_id: int,
        city_update: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.CityCreate:
    db_city = await crud.get_city(db=db, city_id=city_id)

    is_not_city_name_exist = await crud.check_correct_city_name(
        name=city_update.name
    )

    if db_city or is_not_city_name_exist:
        raise HTTPException(
            status_code=400,
            detail="This name is already exist or incorrect name of city!"
        )

    updated_city = await crud.update_city(
        db=db,
        city=db_city,
        city_update=city_update
    )
    return updated_city
