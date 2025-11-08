from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "City"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    additional_info = Column(String, nullable=True)
    temperatures = relationship(
        "Temperature", back_populates="city", cascade="all, delete-orphan"
    )


class Temperature(Base):
    __tablename__ = "Temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(
        Integer, ForeignKey("City.id", ondelete="CASCADE"), index=True, nullable=False
    )
    date_time = Column(String, index=True, nullable=False)
    temperature = Column(Float, nullable=False)
    city = relationship("City", back_populates="temperatures")
