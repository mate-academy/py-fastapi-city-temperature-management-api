from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(
    prefix='/cities',
    tags=['Cities'],
)


@router.post(
    '/',
    response_model=schemas.CityResponse,
)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
) -> schemas.CityResponse:
    try:
        return crud.create_city(
            db=db,
            city=city,
        )
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail='City with this name already exists',
        )


@router.get(
    '/',
    response_model=list[schemas.CityResponse],
)
def read_cities(
    db: Session = Depends(get_db),
) -> list[schemas.CityResponse]:
    return crud.get_cities(db=db)


@router.get(
    '/{city_id}',
    response_model=schemas.CityResponse,
)
def read_city(
    city_id: int,
    db: Session = Depends(get_db),
) -> schemas.CityResponse:
    city = crud.get_city(
        db=db,
        city_id=city_id,
    )

    if city is None:
        raise HTTPException(
            status_code=404,
            detail='City not found',
        )

    return city


@router.put(
    '/{city_id}',
    response_model=schemas.CityResponse,
)
def update_city(
    city_id: int,
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
) -> schemas.CityResponse:
    try:
        updated_city = crud.update_city(
            db=db,
            city_id=city_id,
            city=city,
        )
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail='City with this name already exists',
        )

    if updated_city is None:
        raise HTTPException(
            status_code=404,
            detail='City not found',
        )

    return updated_city


@router.delete(
    '/{city_id}',
    response_model=schemas.CityResponse,
)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
) -> schemas.CityResponse:
    deleted_city = crud.delete_city(
        db=db,
        city_id=city_id,
    )

    if deleted_city is None:
        raise HTTPException(
            status_code=404,
            detail='City not found',
        )

    return deleted_city
