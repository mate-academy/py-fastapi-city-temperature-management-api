from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.dependencies import get_db


router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)


@router.post(
    "",
    response_model=schemas.CityRead,
    status_code=status.HTTP_201_CREATED
)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db)
) -> models.City:
    return crud.create_city(db, city)


@router.get(
    "",
    response_model=list[schemas.CityRead]
)
def read_cities(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> list[models.City]:
    return crud.get_cities(db, skip=skip, limit=limit)


@router.get(
    "/{city_id}",
    response_model=schemas.CityRead
)
def read_city(
    city_id: int,
    db: Session = Depends(get_db)
) -> models.City:
    city = crud.get_city(db, city_id)

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return city


@router.put(
    "/{city_id}",
    response_model=schemas.CityRead
)
def update_city(
    city_id: int,
    city: schemas.CityUpdate,
    db: Session = Depends(get_db)
) -> models.City:
    updated_city = crud.update_city(db, city_id, city)

    if updated_city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return updated_city


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db)
) -> None:
    deleted = crud.delete_city(db, city_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )
