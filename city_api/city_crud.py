from sqlalchemy.orm import Session

from city_api import city_models, city_schemas


def city_create(
        db: Session,
        city: city_schemas.CityCreate
):
    new_city = city_models.DBCity(
        name=city.name,
        additional_info=city.additional_info 
    )
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


def get_city_by_name(
        db: Session,
        name: str
):
    return db.query(city_models.DBCity).filter(city_models.DBCity.name==name).first()


def get_city_list(
        db: Session,
        skip: int | None = None,
        limit: int | None = None
        ):
    queryset = db.query(city_models.DBCity)

    if skip is not None:
        queryset = queryset.offset(skip)

    if limit is not None:
        queryset = queryset.limit(limit)
    
    return queryset.all()


def get_city_by_id(
        db: Session,
        id: int
):
    return db.query(city_models.DBCity).filter(city_models.DBCity.id==id).first()


def update_city_details(
        db: Session,
        city: city_schemas.City,
        new_values: city_schemas.CityUpdate
):
    
    if new_values.name:
        city.name = new_values.name

    if new_values.additional_info:
        city.additional_info = new_values.additional_info
    
    db.commit()
    db.refresh(city)
    return city


def delete_city(
        db: Session,
        city: city_schemas.City
):
    city_name = city.name

    db.delete(city)
    db.commit()
    return {"message": f"Operation success! {city_name} was deleted from DB!" }


