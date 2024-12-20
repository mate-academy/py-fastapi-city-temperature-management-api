from fastapi import FastAPI

from city import router


app = FastAPI()

app.include_router(router.router)


@app.get("/")
def home_page():
    return {"Message": "The server is running"}
