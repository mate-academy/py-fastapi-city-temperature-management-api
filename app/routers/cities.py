from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from app import crud, schemas
from app.database import get_db


router = APIRouter(prefix="/cities", tags=["cities"])


@router.post(
    "",
    response_model=schemas.City,
    status_code=status.HTTP_201_CREATED
)
async def create_city(
    city: schemas.CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await crud.create_city(db, city)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A city with this name already exists",
        )


@router.get("", response_model=list[schemas.City])
async def list_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_cities(db)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    city = await crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    await crud.delete_city(db, city)
