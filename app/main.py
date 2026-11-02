from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.services import fetch_and_store_temperatures

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="City and Weather Management API",
    version="1.0.0",
    description="Додаток FastAPI для управління містами та історією температур."
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Ендпоінти для Міст (Cities) ---

@app.post("/cities", response_model=schemas.CityRead, status_code=status.HTTP_201_CREATED, summary="Створити нове місто")
def create_city(city_in: schemas.CityCreate, db: Session = Depends(get_db)) -> schemas.CityRead:
    return crud.create_city(db, city_in)


@app.get("/cities", response_model=list[schemas.CityRead], summary="Отримати список усіх міст")
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[schemas.CityRead]:
    return crud.get_cities(db, skip=skip, limit=limit)


@app.get("/cities/{city_id}", response_model=schemas.CityRead, summary="Отримати деталі конкретного міста")
def read_city(city_id: int, db: Session = Depends(get_db)) -> schemas.CityRead:
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Місто не знайдено")
    return db_city


@app.put("/cities/{city_id}", response_model=schemas.CityRead, summary="Оновити дані міста")
def update_city(city_id: int, city_in: schemas.CityUpdate, db: Session = Depends(get_db)) -> schemas.CityRead:
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Місто не знайдено")
    return crud.update_city(db, db_city, city_in)


@app.delete("/cities/{city_id}", response_model=schemas.CityRead, summary="Видалити місто")
def delete_city(city_id: int, db: Session = Depends(get_db)) -> schemas.CityRead:
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Місто не знайдено")
    return crud.delete_city(db, db_city)


# --- Ендпоінти для Температур (Temperatures) ---

@app.post("/temperatures/update", response_model=list[schemas.TemperatureRead], summary="Отримати та зберегти поточну температуру для всіх міст")
async def update_temperatures(db: Session = Depends(get_db)) -> list[schemas.TemperatureRead]:
    records = await fetch_and_store_temperatures(db)
    return records


@app.get("/temperatures", response_model=list[schemas.TemperatureRead], summary="Отримати історію температур")
def read_temperatures(city_id: int | None = None, db: Session = Depends(get_db)) -> list[schemas.TemperatureRead]:
    return crud.get_temperatures(db, city_id=city_id)
