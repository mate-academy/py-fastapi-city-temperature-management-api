from datetime import datetime, UTC

from sqlalchemy.orm import Session
from app.models.temperature import Temperature
from app.schemas.temperature import TemperatureCreate


class TemperatureRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, temperature: TemperatureCreate) -> Temperature:
        db_temperature = Temperature(
            city_id=temperature.city_id,
            temperature=temperature.temperature,
            date_time=datetime.now(UTC)
        )
        self.db.add(db_temperature)
        self.db.commit()
        self.db.refresh(db_temperature)
        return db_temperature

    def create_bulk(self, temperatures: list[TemperatureCreate]) -> list[Temperature]:
        current_time = datetime.now(UTC)

        db_temperatures = [
            Temperature(
                city_id=temp.city_id,
                temperature=temp.temperature,
                date_time=current_time
            )
            for temp in temperatures
        ]

        self.db.add_all(db_temperatures)
        self.db.commit()

        for temp in db_temperatures:
            self.db.refresh(temp)

        return db_temperatures

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Temperature]:
        return self.db.query(Temperature).offset(skip).limit(limit).all()

    def get_by_city_id(
            self,
            city_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> list[Temperature]:
        return (
            self.db.query(Temperature)
            .filter(Temperature.city_id == city_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
