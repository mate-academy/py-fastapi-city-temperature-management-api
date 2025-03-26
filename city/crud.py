from fastapi import HTTPException
from sqlalchemy.orm import Session


from city import schemas, models


def get_city_by_id(city_id: int, db: Session):
    return db.query(models.CityDB).filter(models.CityDB.id == city_id).first()

def check_city(city):
    if city is None:
        raise HTTPException(status_code=404, detail="doesn't exist")


def create_city(db: Session, city_data: schemas.CityCreate) -> models.CityDB:
    new_city = models.CityDB(**city_data.model_dump())

    db.add(new_city)
    db.commit()
    db.refresh(new_city)

    return new_city


def get_cities(db: Session):
    return db.query(models.CityDB).all()


def get_city(city_id: int, db: Session):
    return db.query(models.CityDB).filter(models.CityDB.id == city_id).first()


def update_city(city_id: int, db: Session, updated_city):
    city = get_city_by_id(city_id=city_id, db=db)
    check_city(city)
    city.name = updated_city.name
    city.additional_info = updated_city.additional_info
    db.commit()
    db.refresh(city)

    return city

def partial_update_city(city_id: int, db: Session, updated_city):
    city = get_city_by_id(city_id=city_id, db=db)
    check_city(city)

    for key, value in updated_city.dict(exclude_unset=True).items():
        setattr(city, key, value)

    db.commit()
    db.refresh(city)

    return city


def delete_city(city_id: int, db: Session):
    city = get_city_by_id(city_id=city_id, db=db)
    check_city(city)

    db.delete(city)
    db.commit()

    return f"City {city.name} with ID {city.id} has been deleted"
