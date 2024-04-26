from sqlalchemy import Column, Integer, String
from database import Base


class DbCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(1023), nullable=False)
