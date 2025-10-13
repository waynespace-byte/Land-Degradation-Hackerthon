import numpy as np
import pandas as pd
from datetime import datetime
from .. import crud, schemas, models
from sqlalchemy.orm import Session

def calculate_ndvi(nir: float, red: float) -> float:
    if nir + red == 0:
        return 0.0
    return (nir - red) / (nir + red)

def analyze_land(db: Session, land_id: int):
    nir = np.random.uniform(0.4, 0.8)
    red = np.random.uniform(0.1, 0.4)
    ndvi = calculate_ndvi(nir, red)
    
    land = crud.update_land_ndvi(db, land_id, ndvi)
    
    sensors = db.query(models.Sensor).filter(models.Sensor.land_id == land_id).order_by(models.Sensor.timestamp.desc()).limit(5).all()
    if sensors:
        avg_moisture = np.mean([s.moisture for s in sensors]) if sensors else 0
        if ndvi < 0.3 and avg_moisture < 20:
            alert_msg = f"Soil health declining in {land.name}, initiate restoration."
            alert = schemas.Alert(message=alert_msg, land_id=land_id, severity="high")
            crud.create_alert(db, alert)
    
    return ndvi

async def scan_all_lands(db: Session):  # Made async
    lands = crud.get_lands(db)
    for land in lands:
        analyze_land(db, land.id)