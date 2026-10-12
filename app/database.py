from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./cities.db" #location to store the database

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) #mechanism for communication with SQLite

Base = declarative_base() #mechanism for SQLalchemy models/tables

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #creates database session for communication with database