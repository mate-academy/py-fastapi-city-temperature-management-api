from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db


router = APIRouter(
    prefix="/cities",
    tags=["cities"],
)


@router.post(
    "",
    response_model=schemas.City,
    status_code=status.HTTP_201_CREATED,
)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
) -> schemas.City:
    if crud.get_city_by_name(db, city.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City with this name already exists",
        )

    try:
        return crud.create_city(db, city)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City with this name already exists",
        ) from exc


@router.get(
    "",
    response_model=list[schemas.City],
)
def read_cities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[schemas.City]:
    return crud.get_cities(
        db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{city_id}",
    response_model=schemas.City,
)
def read_city(
    city_id: int,
    db: Session = Depends(get_db),
) -> schemas.City:
    city = crud.get_city(db, city_id)

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
) -> schemas.City:
    city = crud.get_city(db, city_id)

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    try:
        return crud.update_city(
            db,
            city,
            city_data,
        )
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City with this name already exists",
        ) from exc


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
) -> None:
    city = crud.get_city(db, city_id)

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    crud.delete_city(db, city)
