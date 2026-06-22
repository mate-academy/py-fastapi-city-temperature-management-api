from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db.database import engine, Base
from app.dependencies import get_db

Base.metadata.create_all(bind=engine)
app = FastAPI()

CurrentSession = Annotated[Session, Depends(get_db)]