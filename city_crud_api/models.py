from database import Base
from sqlalchemy import Column, Integer, String


class City(Base):
    __tablename__ = "City"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(955), nullable=False)
