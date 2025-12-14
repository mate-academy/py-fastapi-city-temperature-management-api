from fastapi import FastAPI
from app import router


app = FastAPI()


app.include_router(router.router)


@app.get("/")
def root() -> dict:
    return {
        "message": "Welcome to City Temperature Management Api"
    }
