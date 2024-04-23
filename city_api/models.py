from sqlalchemy import Column, Integer, String

from database import Base


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(96))
    additional = Column(String(1024))

    def __repr__(self):
        return self.name
