from typing import Optional

from sqlalchemy.orm import Session

from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate


class CityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, city: CityCreate) -> City:
        db_city = City(
            name=city.name,
            additional_info=city.additional_info
        )
        self.db.add(db_city)
        self.db.commit()
        self.db.refresh(db_city)
        return db_city

    def get_all(self, skip: int = 0, limit: int = 100) -> list[City]:
        return self.db.query(City).offset(skip).limit(limit).all()

    def get_by_id(self, city_id: int) -> Optional[City]:
        return self.db.query(City).filter(City.id == city_id).first()

    def get_by_name(self, name: str) -> Optional[City]:
        return self.db.query(City).filter(City.name == name).first()

    def update(self, city_id: int, city_update: CityUpdate) -> Optional[City]:
        db_city = self.db.query(City).filter(City.id == city_id).first()
        if not db_city:
            return None

        update_data = city_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_city, field, value)

        self.db.commit()
        self.db.refresh(db_city)

        return db_city

    def delete(self, city_id: int) -> bool:
        db_city = self.db.query(City).filter(City.id == city_id).first()
        if not db_city:
            return False

        self.db.delete(db_city)
        self.db.commit()

        return True
