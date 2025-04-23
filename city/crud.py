from sqlalchemy.orm import Session
import city.models, city.schemas

def create_city(db: Session, city_data: city.schemas.CityCreate):
    db_city = city.models.City(**city_data.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_cities(db: Session):
    return db.query(city.models.City).all()

def get_city(db: Session, city_id: int):
    return db.query(city.models.City).filter(city.models.City.id == city_id).first()

def update_city(db: Session, city_id: int, city_data: city.schemas.CityUpdate):
    db_city = get_city(db, city_id)
    if db_city:
        for key, value in city_data.dict().items():
            setattr(db_city, key, value)
        db.commit()
        db.refresh(db_city)
    return db_city

def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city
