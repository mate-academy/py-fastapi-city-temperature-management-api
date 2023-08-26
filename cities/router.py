from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import (
    get_db,
    common_city_parameters,
)

from cities import crud, schemas


router = APIRouter()


@router.get(
    "/cities/",
    response_model=list[schemas.City],
)
async def read_cities(
    db: AsyncSession = Depends(get_db),
) -> [list[schemas.City] | list]:
    return await crud.get_all_cities(db=db)


@router.get(
    "/cities/{city_id}/",
    response_model=schemas.City,
)
async def retrieve_city(
    commons: Annotated[dict, Depends(common_city_parameters)],
) -> [schemas.City | Exception]:
    city = await crud.get_city(
        db=commons.get("db"),
        city_id=commons.get("city_id")
    )

    if city:
        return city

    raise HTTPException(
        status_code=404,
        detail="City not found"
    )


@router.post(
    "/cities/",
    response_model=schemas.City,
)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
) -> [schemas.City | Exception]:
    if await crud.get_city_by_name(db=db, city_name=city.name):
        raise HTTPException(
            status_code=400,
            detail="Such city already exists"
        )

    return await crud.create_city(db=db, city=city)


@router.put(
    "/cities/{city_id}/",
    response_model=schemas.City,
)
async def update_city(
    commons: Annotated[dict, Depends(common_city_parameters)],
    new_data:  dict,
) -> [schemas.City | Exception]:
    updated_city = await crud.update_city(
        db=commons.get("db"),
        city_id=commons.get("city_id"),
        new_data=new_data,
    )

    if updated_city:
        return updated_city

    raise HTTPException(
        status_code=404,
        detail="You cannot update city data which not found"
    )


@router.delete(
    "/cities/{city_id}/",
    response_model=schemas.CityDelete,
)
async def delete_city(
    commons: Annotated[dict, Depends(common_city_parameters)],
) -> [schemas.CityDelete | Exception]:
    deleted_city = await crud.delete_city(
        db=commons.get("db"),
        city_id=commons.get("city_id"),
    )

    if deleted_city:
        return deleted_city
    raise HTTPException(
        status_code=404,
        detail="You cannot delete the city which not found"
    )
