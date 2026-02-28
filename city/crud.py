from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from city.models import City


def db_read_cities(
    db: Session
) -> list[City]:
    return db.execute(select(City)).scalars().all()


def db_create_city(
    city: City,
    db: Session
) -> City | None:
    try:
        db.add(city)
        db.commit()
        db.refresh(city)
        return city
    except IntegrityError:
        db.rollback()
        return None


def db_read_city(
    id: int,
    db: Session
) -> City | None:
    return db.execute(select(City).where(City.id == id)).scalar_one_or_none()


def db_update_city(
    id: int,
    city: City,
    db: Session
) -> City | None:
    existing_city = db_read_city(
        id=id,
        db=db
    )
    if existing_city is None:
        return None
    try:
        existing_city.name = city.name
        existing_city.additional_info = city.additional_info
        db.commit()
        db.refresh(existing_city)
        return existing_city
    except IntegrityError:
        db.rollback()
        return None
    except ValueError:
        db.rollback()
        raise


def db_delete_city(
    id: int,
    db: Session
) -> True | False:
    city = db_read_city(
        id=id,
        db=db
    )
    if city is None:
        return False
    db.delete(city)
    db.commit()
    return True
