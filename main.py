import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.name == city.name).first()
    if db_city:
        raise HTTPException(status_code=400, detail="City already exists")
    return crud.create_city(db=db, city=city)

@app.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)


@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    if not crud.delete_city(db, city_id):
        raise HTTPException(status_code=404, detail="City not found")
    return {"detail": "City deleted"}


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    if not cities:
        raise HTTPException(status_code=400, detail="No cities in database")
    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                url = f"https://api.open-meteo.com/v1/forecast?latitude={city.latitude}&longitude={city.longitude}&current_weather=true"
                res = await client.get(url)
                res.raise_for_status()
                temp = res.json()["current_weather"]["temperature"]
                crud.create_temperature(db, city_id=city.id, temp=temp)
            except httpx.HTTPError:
                continue
    return {"detail": "Temperatures updated"}


@app.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id=city_id)
