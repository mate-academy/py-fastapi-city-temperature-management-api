from fastapi import HTTPException
from sqlalchemy.orm import Session

from city import crud


def city_update_validation(
        db: Session,
        city_id: int,
        new_city_name: str,
        new_additional_info: str,
):
    current_city = crud.get_city_by_id(db=db, city_id=city_id)

    if not current_city:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")

    if (
            current_city.name == new_city_name
            and current_city.additional_info == new_additional_info
    ):
        raise HTTPException(status_code=400, detail=f"The content has not changed")

    exists_name = crud.get_city_by_name(db=db, name=new_city_name)

    if exists_name:
        raise HTTPException(status_code=400, detail=f"City with that name already exist")
