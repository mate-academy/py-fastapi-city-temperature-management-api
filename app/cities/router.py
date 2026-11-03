from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.cities import crud, schemas
from app.dependencies import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


def get_city_or_404(city_id: int, db: Session = Depends(get_db)):
    """Залежність: повертає місто або 404."""
    city = crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "City not found")
    return city


@router.post(
    "",
    response_model=schemas.City,
    status_code=status.HTTP_201_CREATED
)
def create_city(data: schemas.CityCreate, db: Session = Depends(get_db)):
    if crud.get_city_by_name(db, data.name):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "City with this name already exists"
        )
    return crud.create_city(db, data)


@router.get("", response_model=list[schemas.City])
def list_cities(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_cities(db, skip, limit)


@router.get("/{city_id}", response_model=schemas.City)
def read_city(city=Depends(get_city_or_404)):
    return city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    data: schemas.CityUpdate,
    city=Depends(get_city_or_404),
    db: Session = Depends(get_db),
):
    if (
        data.name
        and data.name != city.name
        and crud.get_city_by_name(db, data.name)
    ):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "City with this name already exists",
        )
    return crud.update_city(db, city, data)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city=Depends(get_city_or_404), db: Session = Depends(get_db)):
    crud.delete_city(db, city)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
