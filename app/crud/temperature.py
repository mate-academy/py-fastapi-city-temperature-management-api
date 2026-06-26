from sqlalchemy.orm import Session

from app.models.temperature import Temperature


def create_temperature(db: Session, city_id: int, date_time, temperature: float):
    db_temp = Temperature(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature,
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def get_temperatures(db: Session):
    return db.query(Temperature).all()


def get_temperatures_by_city(db: Session, city_id: int):
    return db.query(Temperature).filter(
        Temperature.city_id == city_id
    ).all()
