from sqlalchemy.orm import Session
from city_temp import models, schemas


def get_cities(db: Session):
  return db.query(models.City).all()


def get_city(db: Session, city_id: int):
  return db.query(models.City).filter(models.City.id == city_id).first()


def create_city(db: Session, city: schemas.CityCreate):
  db_city = models.City(
      name=city.name, additional_info=city.additional_info
  )
  db.add(db_city)
  db.commit()
  db.refresh(db_city)
  return db_city


def get_temperatures(db: Session, city_id: int | None = None):
  query = db.query(models.Temperature)
  if city_id is not None:
    query = query.filter(models.Temperature.city_id == city_id)
  return query.all()


def create_temperature_record(db: Session, city_id: int, temperature: float):
  db_temp = models.Temperature(city_id=city_id, temperature=temperature)
  db.add(db_temp)
  db.commit()
  db.refresh(db_temp)
  return db_temp
