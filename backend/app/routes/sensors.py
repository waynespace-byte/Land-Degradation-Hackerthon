from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import crud, schemas, auth, models
from ..database import get_db

router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.post("/", response_model=schemas.Sensor)
def create_sensor(sensor: schemas.SensorCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Check ownership
    land = db.query(models.Land).filter(models.Land.id == sensor.land_id, models.Land.user_id == current_user.id).first()
    if not land:
        raise HTTPException(status_code=403, detail="Unauthorized access to land")
    # Create full Sensor model
    db_sensor = models.Sensor(
        land_id=sensor.land_id,
        moisture=sensor.moisture,
        ph=sensor.ph,
        temperature=sensor.temperature
    )
    return crud.create_sensor(db=db, sensor=db_sensor)

@router.get("/", response_model=List[schemas.Sensor])
def read_sensors(land_id: Optional[int] = Query(None), current_user: Optional[models.User] = Depends(auth.get_current_user_optional), db: Session = Depends(get_db)):
    query = db.query(models.Sensor).join(models.Land)
    if current_user:
        query = query.filter(models.Land.user_id == current_user.id)
    if land_id:
        query = query.filter(models.Sensor.land_id == land_id)
    return query.all()  # Empty list if no user (avoids 403 for Charts.js)