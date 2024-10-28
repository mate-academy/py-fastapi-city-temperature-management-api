from sqlalchemy import Column, Integer, String

from database import Base


class City(Base):
    __tablename__ = "city"

    id: int = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(String(700), nullable=False)

    def __str__(self):
        return self.name
