from fastapi import FastAPI
from routes import cities, temperatures


app = FastAPI(title="City Temperature API")

app.include_router(cities.router)
app.include_router(temperatures.router)
