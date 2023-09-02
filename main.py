from fastapi import FastAPI

from temperature import router

app = FastAPI()

app.include_router(router.router)


@app.get("/")
def root() -> dict:
    return {"message": "City temperature management"}