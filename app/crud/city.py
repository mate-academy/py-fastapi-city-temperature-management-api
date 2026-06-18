from sqlalchemy.orm import Session
from app.models.models import City
from app.schemas.schemas import CityCreate, CityUpdate


def get_city(db: Session, city_id: int) -> City | None:
    """Return a single city by primary key, or None if not found."""
    return db.query(City).filter(City.id == city_id).first()


def get_city_by_name(db: Session, name: str) -> City | None:
    """Return a city matched by name (case-sensitive), or None."""
    return db.query(City).filter(City.name == name).first()


def get_cities(db: Session, skip: int = 0, limit: int = 100) -> list[City]:
    """Return a paginated list of all cities."""
    return db.query(City).offset(skip).limit(limit).all()


def create_city(db: Session, city: CityCreate) -> City:
    """Persist a new city and return the created ORM object."""
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_id: int, city_data: CityUpdate) -> City | None:
    """Update an existing city's fields. Returns None if city does not exist."""
    db_city = get_city(db, city_id)
    if db_city is None:
        return None
    update_data = city_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_city, field, value)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> City | None:
    """Delete a city by ID. Returns the deleted object, or None if not found."""
    db_city = get_city(db, city_id)
    if db_city is None:
        return None
    db.delete(db_city)
    db.commit()
    return db_city