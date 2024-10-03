from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.city_crud import get_cities, create_city, delete_city
from app.models import City, Temperature
from app.temperature import update_temperatures

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities/")
def create_city_endpoint(name: str, additional_info: str, db: Session = Depends(get_db)):
    return create_city(db, City(name=name, additional_info=additional_info))


@app.get("/cities/")
def read_cities(db: Session = Depends(get_db)):
    return get_cities(db)


@app.delete("/cities/{city_id}")
def delete_city_endpoint(city_id: int, db: Session = Depends(get_db)):
    return delete_city(db, city_id)


@app.post("/temperatures/update")
async def update_temperatures_endpoint(db: Session = Depends(get_db)):
    await update_temperatures(db)
    return {"status": "updated"}


@app.get("/temperatures/")
def get_temperatures(db: Session = Depends(get_db)):
    return db.query(Temperature).all()
