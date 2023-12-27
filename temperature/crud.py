from sqlalchemy.orm import Session
import models, schemas


def all_temperature(db: Session):
    return db.query(models.Temperature).all()


def all_temperature_by_city_id(db: Session, city_id: int):
    return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()
