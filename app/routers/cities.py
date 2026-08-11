from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.crud import city as city_crud
from app.database import get_database
from app.schemas.city import CityCreate, CityRead


router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("/", response_model=list[CityRead])
def get_cities(
    database: Annotated[Session, Depends(get_database)],
) -> list[CityRead]:
    return city_crud.get_cities(database=database)


@router.post(
    "/",
    response_model=CityRead,
    status_code=status.HTTP_201_CREATED,
)
def create_city(
    city: CityCreate,
    database: Annotated[Session, Depends(get_database)],
) -> CityRead:
    return city_crud.create_city(database=database, city=city)


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_city(
    city_id: int,
    database: Annotated[Session, Depends(get_database)],
) -> Response:
    city = city_crud.get_city_by_id(database=database, city_id=city_id)

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    city_crud.delete_city(database=database, city=city)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
