from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
)

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from starlette import status

from .schemas import (
    CityCreate,
    CityRead,
    CityUpdate,
)

from models import get_session, DBCity


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()


@router.post("/cities", response_model=CityRead)
def create_city(session: SessionDep, city: CityCreate):
    try:
        obj = DBCity(**city.model_dump())
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    except IntegrityError:
        session.rollback()
        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="City with this name already exists",

        )


@router.get("/cities", response_model=list[CityRead])
def list_cities(session: SessionDep):
    stmt = select(DBCity)
    return session.scalars(stmt).all()


@router.get("/cities/{city_id}", response_model=CityRead)
def get_city(session: SessionDep, city_id: int):
    city_obj = session.get(DBCity, city_id)

    if city_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    return city_obj


@router.put("/cities/{city_id}", response_model=CityRead)
def update_city(session: SessionDep, city_id: int, city: CityUpdate):
    city_obj = session.get(DBCity, city_id)

    if city_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    data = city.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(city_obj, field, value)

    session.commit()
    session.refresh(city_obj)
    return city_obj


@router.delete("/cities/{city_id}")
def delete_city(session: SessionDep, city_id: int):
    city_obj = session.get(DBCity, city_id)

    if city_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    session.delete(city_obj)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
