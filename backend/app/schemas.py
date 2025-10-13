from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    name: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Land Schemas
class LandCreate(BaseModel):
    name: str
    location: str
    # No user_id here—set server-side from authenticated user

class Land(LandCreate):
    id: int
    ndvi: float = 0.0
    is_degraded: bool = False
    user_id: int  # Included in response (set server-side)
    created_at: datetime

    class Config:
        from_attributes = True

# Sensor Schemas
class SensorCreate(BaseModel):
    land_id: int
    moisture: float
    ph: float
    temperature: float

class Sensor(SensorCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Alert Schemas
class Alert(BaseModel):
    id: int
    message: str
    land_id: int
    severity: str = "medium"
    resolved: bool = False
    timestamp: datetime

    class Config:
        from_attributes = True

# Analysis Response
class AnalysisResponse(BaseModel):
    ndvi: float
    degraded: bool