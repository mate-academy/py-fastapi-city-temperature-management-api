from fastapi import FastAPI

from database import engine
from models import Base
from routes import router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(router)
