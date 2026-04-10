from fastapi import APIRouter
from sqlalchemy import select
from fastapi import Depends
from sqlalchemy.orm import Session
from city import schemas, crud, models
from city.crud import fetch_temperature
from database.deps import get_db
from datetime import datetime, timezone

city_router = APIRouter()

@city_router.get("/cities", response_model=list[schemas.CitySchemaDetail])
def get_cities(db: Session = Depends(get_db), limit: int | None = None):
    return crud.get_city(db=db, limit=limit)


@city_router.post("/cities", response_model=schemas.CitySchemaDetail)
def create_city(city: schemas.City, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@city_router.get("/cities/{city_id}", response_model=schemas.CitySchemaDetail)
def get_city(city_id: int, db: Session = Depends(get_db)):
    return crud.get_city_by_id(db=db, city_id=city_id)


@city_router.put("/cities/{city_id}", response_model=schemas.CitySchemaDetail)
def update_city(city_id: int, city: schemas.City, db: Session = Depends(get_db)):
    return crud.city_update(db=db, city_id=city_id, city=city)


@city_router.delete("/cities/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    return crud.city_delete(db=db, city_id=city_id)

@city_router.post("/temperatures/update")
async def temperatures_update(db: Session = Depends(get_db)):
    cities = db.scalars(select(models.City)).all()

    for city in cities:
        temp = await fetch_temperature(city.name)

        db_temp = models.Temperature(
            city_id=city.id,
            date_time=datetime.now(timezone.utc),
            temperature=temp
        )

        db.add(db_temp)

    db.commit()
    return {"message": "Temperatures updated"}


@city_router.get("/temperatures", response_model=list[schemas.Temperature])
def get_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = select(models.Temperature)

    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)

    return db.scalars(query).all()