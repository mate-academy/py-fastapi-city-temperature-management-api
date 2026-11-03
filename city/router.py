from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from city import crud, models, schemas
from dependencies import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


def get_city_or_404(
    city_id: int, db: Session = Depends(get_db)
) -> models.DBCity:
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    return db_city


def ensure_name_is_free(
    db: Session, name: str, city_id: int | None = None
) -> None:
    db_city = crud.get_city_by_name(db=db, name=name)

    if db_city is not None and db_city.id != city_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists",
        )


@router.get("", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.post(
    "", response_model=schemas.City, status_code=status.HTTP_201_CREATED
)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    ensure_name_is_free(db=db, name=city.name)

    return crud.create_city(db=db, city=city)


@router.get("/{city_id}", response_model=schemas.City)
def read_city(db_city: models.DBCity = Depends(get_city_or_404)):
    return db_city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city: schemas.CityUpdate,
    db_city: models.DBCity = Depends(get_city_or_404),
    db: Session = Depends(get_db),
):
    ensure_name_is_free(db=db, name=city.name, city_id=db_city.id)

    return crud.update_city(db=db, db_city=db_city, city=city)


@router.delete("/{city_id}", response_model=schemas.City)
def delete_city(
    db_city: models.DBCity = Depends(get_city_or_404),
    db: Session = Depends(get_db),
):
    return crud.delete_city(db=db, db_city=db_city)
