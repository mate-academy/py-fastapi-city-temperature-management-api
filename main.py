from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

# Simulated database to store city data
city_db: Dict[int, dict] = {}


class City(BaseModel):
    id: int
    name: str
    additional_info: Optional[str] = None


@app.post("/cities/", response_model=City)
def create_city(city: City):
    if city.id in city_db:
        raise HTTPException(status_code=400, detail="City with this id already exists")
    city_db[city.id] = city.model_dump()
    return city


@app.get("/cities/{city_id}", response_model=City)
def read_city(city_id: int):
    city = city_db.get(city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return City(**city)


@app.put("/cities/{city_id}", response_model=City)
def update_city(city_id: int, city: City):
    if city_id not in city_db:
        raise HTTPException(status_code=404, detail="City not found")
    city_db[city_id] = city.dict()
    return City(**city_db[city_id])


@app.delete("/cities/{city_id}", response_model=City)
def delete_city(city_id: int):
    city = city_db.pop(city_id, None)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return City(**city)


@app.get("/cities/", response_model=List[City])
def list_cities():
    return [City(**city_data) for city_data in city_db.values()]
