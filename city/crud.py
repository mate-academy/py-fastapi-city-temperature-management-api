from fastapi import HTTPException
from sqlalchemy.orm import Session

from city import schemas, models


def get_all_cities(db: Session) -> list[schemas.City]:
    return db.query(models.City).all()


def create_city(
        db: Session,
        city_schema: schemas.CityCreateUpdate
) -> schemas.City:
    db_city = models.City(
        **city_schema.model_dump()
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city_by_id(db: Session, city_id: int) -> schemas.City:
    return db.query(models.City).filter(models.City.id == city_id).first()


def city_exists(db: Session, city_id: int) -> None:
    if not get_city_by_id(db=db, city_id=city_id):
        raise HTTPException(
            status_code=404,
            detail=f"City with id {city_id} does not exist"
        )


def get_city_by_name(db: Session, city_name: str) -> schemas.City | None:
    return db.query(models.City).filter(models.City.name == city_name).first()


def delete_city(db: Session, city_id: int) -> dict[str, bool]:
    db_city = get_city_by_id(db=db, city_id=city_id)
    db.delete(db_city)
    db.commit()
    return {"ok": True}


def update_city(
    db: Session,
    city_id: int,
    city_schema: schemas.CityCreateUpdate
) -> schemas.City:
    db_city = get_city_by_id(db=db, city_id=city_id)

    db_city.name = city_schema.name
    db_city.additional_info = city_schema.additional_info

    db.commit()
    db.refresh(db_city)
    return db_city
