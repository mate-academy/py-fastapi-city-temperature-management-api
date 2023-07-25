from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Replace "sqlite:///./cities.db" with your desired database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./cities.db"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create the Base class to be used for declarative models
Base = declarative_base()

# Create a SessionLocal class to handle database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
