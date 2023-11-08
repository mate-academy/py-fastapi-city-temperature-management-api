from fastapi import FastAPI
from city.router import router as city_router
from temperature.router import router as temperature_router

app = FastAPI()

app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
