from sqlalchemy.orm import Session

from app.schemes.city import CityCreate, CityUpdate, CityResponse
from app.db.models import CityModel
from app.exeptions import CityNotFound, CityAlreadyExist


def create_city(db: Session, data: CityCreate) -> CityResponse:
    if db.query(CityModel).filter(CityModel.name == data.name).first():
        raise CityAlreadyExist(f"City {data.name} already exist")

    db_city = CityModel(**data.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return CityResponse.model_validate(db_city)


def get_all_cities(
        db: Session,
        skip: int = 0,
        limit: int = 100) -> list[CityResponse]:
    db_city = db.query(CityModel).offset(skip).limit(limit).all()
    return [CityResponse.model_validate(city) for city in db_city]


def get_city_by_id(db: Session, city_id: int) -> CityResponse:
    db_city = (
        db.query(CityModel)
        .filter(CityModel.id == city_id)
        .first()
    )

    if not db_city:
        raise CityNotFound(f"City with id {city_id} not found")

    return CityResponse.model_validate(db_city)


def get_city_by_name(db: Session, city_name: str) -> CityResponse:
    db_city = (
        db.query(CityModel)
        .filter(CityModel.name == city_name)
        .first()
    )

    if not db_city:
        raise CityNotFound(f"City with name {city_name} not found")

    return CityResponse.model_validate(db_city)


def update_city(db: Session, city_id: int, data: CityUpdate) -> CityResponse:
    db_city = db.query(CityModel).filter(CityModel.id == city_id).first()

    if not db_city:
        raise CityNotFound(f"City with id {city_id} not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_city, key, value)

    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return CityResponse.model_validate(db_city)


def delete_city(db: Session, city_id: int) -> bool:
    db_city = (
        db.query(CityModel)
        .filter(CityModel.id == city_id)
        .first()
    )

    if not db_city:
        raise CityNotFound(f"City with id {city_id} not found")

    db.delete(db_city)
    db.commit()
    return True
