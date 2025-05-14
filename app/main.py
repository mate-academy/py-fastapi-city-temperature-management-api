from fastapi import FastAPI

from api.routes.cities import router as city_router
from api.routes.temperatures import router as temperature_router
	
app = FastAPI()

app.include_router(city_router)
app.include_router(temperature_router)
	
	
@app.get("/")
def root():
    return {"message": "Hello World"}
