from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    client = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    light_level = Column(Float, nullable=True)