from sqlalchemy.orm import Session
from passlib.context import CryptContext  # Moved to top (was inside function)
from typing import Optional  # Added: Fixes the Optional underline/type hint issue
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Global instance (was local)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password[:72])
    db_user = models.User(name=user.name, email=user.email, role=user.role, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_sensor(db: Session, sensor: models.Sensor):
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor
def create_land(db: Session, land: models.Land):
    db.add(land)
    db.commit()
    db.refresh(land)
    return land

def get_lands(db: Session, user_id: int = None):
    query = db.query(models.Land)
    if user_id:
        query = query.filter(models.Land.user_id == user_id)
    return query.all()

def update_land_ndvi(db: Session, land_id: int, ndvi: float):
    land = db.query(models.Land).filter(models.Land.id == land_id).first()
    if land:
        land.ndvi = ndvi
        land.is_degraded = ndvi < 0.3
        db.commit()
        return land
    return None

def create_alert(db: Session, alert: schemas.Alert):
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_alerts(db: Session, land_id: Optional[int] = None):
    query = db.query(models.Alert).filter(models.Alert.resolved == False)
    if land_id:
        query = query.filter(models.Alert.land_id == land_id)
    return query.all()