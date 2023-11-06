from sqlalchemy.orm import Session

from temperature import models, schemas


def create_update_temperatures(db: Session):
    pass


def get_temperatures(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        city_id: int = None
):
    query = db.query(models.Temperature).offset(skip).limit(limit).all()
    if city_id:
        query = (
            db.query(models.Temperature)
            .filter(models.Temperature.city_id == city_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    return query
