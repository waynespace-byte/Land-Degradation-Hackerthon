from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)  # Added length: 255
    email = Column(String(255), unique=True, index=True)  # Added length: 255
    role = Column(String(50))  # Added length: 50 (farmer/ngo/policymaker)
    password_hash = Column(String(255))  # Added length: 255 (hashed)
    created_at = Column(DateTime, default=datetime.utcnow)

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, index=True)
    land_id = Column(Integer, ForeignKey("lands.id"))
    moisture = Column(Float)
    ph = Column(Float)
    temperature = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    land = relationship("Land", back_populates="sensors")

class Land(Base):
    __tablename__ = "lands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)  # Added length: 255
    location = Column(String(100))  # Added length: 100 (lat,lon string)
    ndvi = Column(Float, default=0.0)
    is_degraded = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="lands")
    sensors = relationship("Sensor", back_populates="land")
    created_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(500))  # Added length: 500 (alert messages)
    land_id = Column(Integer, ForeignKey("lands.id"))
    severity = Column(String(20), default="medium")  # Added length: 20 (low/medium/high)
    resolved = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    land = relationship("Land")

User.lands = relationship("Land", back_populates="user")