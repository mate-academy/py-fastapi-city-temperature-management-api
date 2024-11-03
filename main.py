from fastapi import FastAPI

from application import router


app = FastAPI()

app.include_router(router.router)


@app.get("/")
def root() -> dict:
    return {"message": "Welcome"}
