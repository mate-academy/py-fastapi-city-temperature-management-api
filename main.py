from fastapi import FastAPI

from city_crud_api.router import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
