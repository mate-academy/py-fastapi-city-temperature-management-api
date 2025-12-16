from fastapi import FastAPI
from app import router as app_router
app = FastAPI()

app.include_router(app_router.router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
