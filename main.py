from fastapi import FastAPI

import router_weather

app = FastAPI()

app.include_router(router_weather.router)
@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}