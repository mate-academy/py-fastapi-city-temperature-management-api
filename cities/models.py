from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, index=True)
    additional_info = Column(String(500), index=True)

    temperature = relationship("Temperature", uselist=False)
