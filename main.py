from fastapi import FastAPI
from city import router as city_router
from temperature import router as temp_router

app = FastAPI()
app.include_router(city_router.router)
app.include_router(temp_router.router)


@app.get("/")
def root():
    return {"message": "Hello world!"}
