from sqlalchemy.orm import Session

from app.models import City, Temperature


def create_city(db: Session, name: str, info: str):
    city = City(
        name=name,
        additional_info=info
    )

    db.add(city)
    db.commit()
    db.refresh(city)

    return city


def get_cities(db: Session):
    return db.query(City).all()


def get_city(db: Session, city_id: int):
    return (
        db.query(City)
        .filter(City.id == city_id)
        .first()
    )


def delete_city(db: Session, city_id: int):
    city = get_city(db, city_id)

    if city:
        db.delete(city)
        db.commit()

    return city


def create_temperature(
    db: Session,
    city_id: int,
    value: float,
    date_time
):
    temperature = Temperature(
        city_id=city_id,
        temperature=value,
        date_time=date_time
    )

    db.add(temperature)
    db.commit()
    db.refresh(temperature)

    return temperature
