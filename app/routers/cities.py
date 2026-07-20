from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud import city as city_crud
from app.database import get_db
from app.schemas.city import City, CityCreate, CityUpdate

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("", response_model=City, status_code=status.HTTP_201_CREATED)
def create_city(
    city_data: CityCreate,
    db: Session = Depends(get_db),
) -> City:
    if city_crud.get_city_by_name(db, city_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists",
        )

    try:
        return city_crud.create_city(db, city_data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create city",
        ) from exc


@router.get("", response_model=list[City])
def list_cities(db: Session = Depends(get_db)) -> list[City]:
    return city_crud.get_cities(db)


@router.get("/{city_id}", response_model=City)
def get_city(city_id: int, db: Session = Depends(get_db)) -> City:
    city = city_crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return city


@router.put("/{city_id}", response_model=City)
def update_city(
    city_id: int,
    city_data: CityUpdate,
    db: Session = Depends(get_db),
) -> City:
    city = city_crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    if city_data.name is not None:
        city_with_same_name = city_crud.get_city_by_name(db, city_data.name)
        if city_with_same_name and city_with_same_name.id != city_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="City with this name already exists",
            )

    return city_crud.update_city(db, city, city_data)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
) -> Response:
    city = city_crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    city_crud.delete_city(db, city)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
