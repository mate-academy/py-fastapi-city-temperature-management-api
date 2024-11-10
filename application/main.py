from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from application.database import SessionLocal, engine, Base
from application import models, schemas, crud, temperature


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@app.get("/cities", response_model=list[schemas.City])
def get_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_cities(db=db, skip=skip, limit=limit)


@app.get("/cities/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


def update_city(db: Session, city_id: int, city: schemas.CityCreate):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        return None
    db_city.name = city.name
    db_city.description = city.description
    db.commit()
    db.refresh(db_city)

    return db_city


@app.delete("/cities/{city_id}", response_model=dict)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    success = crud.delete_city(db=db, city_id=city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return {"success": True, "message": f"City with ID {city_id} has been deleted."}


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    try:
        await temperature.update_temperatures(db)
        return {"message": "Temperatures updated successfully"}
    except Exception as e:
        print(f"Error updating temperatures: {e}")
        raise HTTPException(status_code=500, detail="Failed to update temperatures")


@app.get("/temperatures", response_model=list[schemas.Temperature])
def get_temperatures(city_id: int = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(models.Temperature)

    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)

    return query.offset(skip).limit(limit).all()


@app.get("/temperatures", response_model=list[schemas.Temperature])
def get_temperatures_by_city(city_id: int, db: Session = Depends(get_db)):
    return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()
