from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from city import crud, models, schemas
from city.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management API")


@app.get("/", tags=["health"])
async def root() -> dict[str, str]:
    return {"message": "City Temperature Management API"}


@app.post("/cities", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)) -> models.City:
    return crud.create_city(db=db, city=city)


@app.get("/cities", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)) -> list[models.City]:
    return crud.get_cities(db=db)


@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)) -> models.City:
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return db_city


@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: Session = Depends(get_db),
) -> models.City:
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return crud.update_city(db=db, db_city=db_city, city_update=city_update)


@app.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)) -> Response:
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")

    crud.delete_city(db=db, db_city=db_city)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
