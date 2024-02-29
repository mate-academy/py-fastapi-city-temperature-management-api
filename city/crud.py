from sqlalchemy.orm import Session

from . import models, schemas


def get_all_cities(db: Session,
                   ) -> list[models.DBCity]:
    return (db
            .query(models.DBCity)
            .all()
            )


def get_city_by_name(db: Session,
                     name: str,
                     ) -> models.DBCity | None:
    return (db
            .query(models.DBCity)
            .filter(models.DBCity.name == name)
            .first()
            )


def get_city_by_id(db: Session,
                   city_id: int,
                   ) -> models.DBCity | None:
    return (db
            .query(models.DBCity)
            .filter(models.DBCity.id == city_id)
            .first()
            )


def create_city(db: Session,
                city: schemas.CityCreate,
                ) -> models.DBCity:
    db_city = models.DBCity.model_dump(city)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(db: Session,
                city_id: int,
                city_data: schemas.CityBase,
                ) -> models.DBCity | None:
    city = get_city_by_id(db=db, city_id=city_id)
    if not city:
        return None
    for attr, value in city_data.model_dump().items():
        setattr(city, attr, value)
    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session,
                city_id: int,
                ) -> None:
    (db
     .query(models.DBCity)
     .filter(models.DBCity.id == city_id)
     .delete()
     )
    db.commit()
