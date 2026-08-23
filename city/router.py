from fastapi import APIRouter, HTTPException

from city import crud, schemas

from dependencies import PaginationDep, DB

router = APIRouter()


@router.get(
    "/cities/",
    response_model=list[schemas.City],
    responses={
        200: {"description": "List of cities returned successfully"},
    },
)
async def read_cities(
    db: DB,
    pagination: PaginationDep,
):
    return await crud.get_all_cities(db=db, pagination=pagination)


@router.post(
    "/cities/",
    response_model=schemas.City,
    status_code=201,
    responses={
        201: {"description": "City created successfully"},
        422: {"description": "Validation error in request body"},
    },
)
async def create_city(city: schemas.CityCreate, db: DB):
    return await crud.create_city(city=city, db=db)


@router.get(
    "/cities/{city_id}/",
    response_model=schemas.City,
    responses={
        200: {"description": "City found and returned"},
        404: {"description": "City not found"},
    },
)
async def read_city(
    city_id: int,
    db: DB,
):
    try:
        return await crud.get_city(
            db=db,
            city_id=city_id,
        )
    except crud.CityNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )


@router.put(
    "/cities/{city_id}/",
    response_model=schemas.City,
    responses={
        200: {"description": "City updated successfully"},
        404: {"description": "City with the given id does not exist"},
        422: {"description": "Validation error in request body"},
    },
)
async def update_city(city_id: int, city: schemas.CityCreate, db: DB):
    try:
        return await crud.update_city(
            db=db,
            city_id=city_id,
            city=city,
        )
    except crud.CityNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )


@router.delete(
    "/cities/{city_id}/",
    status_code=204,
    responses={
        204: {"description": "City deleted successfully"},
        404: {"description": "City with the given id does not exist"},
    },
)
async def delete_city(city_id: int, db: DB):

    try:
        await crud.delete_city(
            db=db,
            city_id=city_id,
        )
    except crud.CityNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )
