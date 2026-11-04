from sqlalchemy.orm import Session

from city import models


def get_all_city_names(db: Session):
    cities = db.query(models.DBCity.name).all()
    return [city[0] for city in cities]
