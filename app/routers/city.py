from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.database.models.city import City
from app.database.session import get_db
from app.schemas.city import (
    CityCreateSchema,
    CityResponseSchema,
    CityUpdateSchema,
    PaginatedCityResponseSchema,
)

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post(
    "/", response_model=CityResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_city(
    city_data: CityCreateSchema, db: Session = Depends(get_db)
) -> CityResponseSchema:
    existing_city = db.query(City).filter_by(name=city_data.name).first()

    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City with name {city_data.name} already exists",
        )

    new_city = City(**city_data.model_dump())
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return CityResponseSchema.model_validate(new_city)


@router.get("/", response_model=PaginatedCityResponseSchema)
def get_list_of_cities(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PaginatedCityResponseSchema:
    cities = db.query(City).offset((page - 1) * per_page).limit(per_page).all()

    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities found",
        )

    city_list = [CityResponseSchema.model_validate(city) for city in cities]

    total_items = db.query(City).count()
    total_pages = (total_items + per_page - 1) // per_page

    base_url = str(request.base_url) + "cities/"

    return PaginatedCityResponseSchema(
        cities=city_list,
        total_items=total_items,
        total_pages=total_pages,
        prev_page=(
            f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
        ),
        next_page=(
            f"{base_url}?page={page + 1}&per_page={per_page}"
            if page < total_pages
            else None
        ),
    )


@router.get("/{city_id}", response_model=CityResponseSchema)
def get_single_city(city_id: int, db: Session = Depends(get_db)) -> CityResponseSchema:
    city = db.query(City).filter_by(id=city_id).first()

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found",
        )

    return CityResponseSchema.model_validate(city)


@router.put("/{city_id}", response_model=CityResponseSchema)
def update_city(
    city_id: int, city_data: CityUpdateSchema, db: Session = Depends(get_db)
) -> CityResponseSchema:
    city = db.query(City).filter_by(id=city_id).first()

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found",
        )

    for key, value in city_data.model_dump().items():
        setattr(city, key, value)

    db.commit()
    db.refresh(city)
    return CityResponseSchema.model_validate(city)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)) -> None:
    city = db.query(City).filter_by(id=city_id).first()

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found",
        )

    db.delete(city)
    db.commit()
