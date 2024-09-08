from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud, schemas
from dependencies import get_db, pagination_params

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(pagination_params),
) -> list[schemas.City]:
    return crud.get_cities_list(
        db=db, skip=pagination["skip"], limit=pagination["limit"]
    )


@router.post(
    "/cities/", response_model=schemas.City, status_code=status.HTTP_201_CREATED
)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    try:
        return await crud.create_city(db=db, city=city)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)) -> schemas.City:
    db_city = crud.get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int, city: schemas.CityUpdate, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    db_city = crud.update_city_by_id(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return db_city


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)) -> schemas.City:
    db_city = crud.delete_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return db_city
