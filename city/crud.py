# POST /cities: Create a new city.
# GET /cities: Get a list of all cities.
# Optional: GET /cities/{city_id}: Get the details of a specific city.
# Optional: PUT /cities/{city_id}: Update the details of a specific city.
# DELETE /cities/{city_id}: Delete a specific city.

from sqlalchemy.orm import Session

from city import models, schemas


def get_all_cities(db: Session):
    return db.query(models.DBCity).all()


def get_city(db: Session, city_id: int) -> list[schemas.City]:
    return db.query(models.DBCity).filter(
        models.DBCity.id == city_id
    ).first()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_id: int, city_update: schemas.CityUpdate):
    db_city = get_city(db=db, city_id=city_id)
    if db_city:
        for key, value in city_update.model_dump().items():
            setattr(db_city, key, value)
        db.commit()
        db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city(db=db, city_id=city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city
