from typing import Union

from fastapi import FastAPI

from city import routers as city_router

app = FastAPI()

app.include_router(city_router.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
