from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
)


@router.post(
    "",
    response_model=schemas.City,
    status_code=status.HTTP_201_CREATED,
)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    existing_city = crud.get_city_by_name(
        db=db,
        name=city.name,
    )

    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists",
        )

    return crud.create_city(
        db=db,
        city=city,
    )


@router.get(
    "",
    response_model=list[schemas.City],
)
def get_cities(
    db: Session = Depends(get_db),
):
    return crud.get_cities(db=db)


@router.get(
    "/{city_id}",
    response_model=schemas.City,
)
def get_city(
    city_id: int,
    db: Session = Depends(get_db),
):
    city = crud.get_city(
        db=db,
        city_id=city_id,
    )

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    return city


@router.put(
    "/{city_id}",
    response_model=schemas.City,
)
def update_city(
    city_id: int,
    city_data: schemas.CityUpdate,
    db: Session = Depends(get_db),
):
    city = crud.get_city(
        db=db,
        city_id=city_id,
    )

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    existing_city = crud.get_city_by_name(
        db=db,
        name=city_data.name,
    )

    if (
        existing_city
        and existing_city.id != city_id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists",
        )

    return crud.update_city(
        db=db,
        city=city,
        city_data=city_data,
    )


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
):
    city = crud.get_city(
        db=db,
        city_id=city_id,
    )

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    crud.delete_city(
        db=db,
        city=city,
    )
