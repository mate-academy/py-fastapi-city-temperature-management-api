from fastapi import FastAPI

from app import routers as app_router


app = FastAPI()

app.include_router(app_router.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
