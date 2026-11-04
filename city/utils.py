from sqlalchemy.orm import Session
from city import models


def get_city_by_name(db: Session, name: str):
    return db.query(models.DBCity).filter(models.DBCity.name == name).first()
