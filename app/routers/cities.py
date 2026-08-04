from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import City as CityModel
from app.schemas import City, CityCreate


router = APIRouter(
    prefix="/cities",
    tags=["cities"],
)


@router.post(
    "",
    response_model=City,
    status_code=status.HTTP_201_CREATED,
)
def create_city(
    city_data: CityCreate,
    database: Session = Depends(get_db),
):
    city = CityModel(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )

    database.add(city)
    database.commit()
    database.refresh(city)

    return city


@router.get(
    "",
    response_model=list[City],
)
def get_cities(
    database: Session = Depends(get_db),
):
    query = select(CityModel)

    cities = database.scalars(query).all()

    return cities


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_city(
    city_id: int,
    database: Session = Depends(get_db),
):
    city = database.get(
        CityModel,
        city_id,
    )

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    database.delete(city)
    database.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
