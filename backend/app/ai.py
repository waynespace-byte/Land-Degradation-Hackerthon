from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models, crud
from datetime import datetime, timedelta
import random  # For demo NDVI (random 0-1; replace with real AI in prod)

def analyze_land(db: Session, land_id: int):
    # Get land and recent sensors (last 24h for demo)
    land = db.query(models.Land).filter(models.Land.id == land_id).first()
    if not land:
        return 0.0  # No land

    recent_sensors = db.query(models.Sensor).filter(
        models.Sensor.land_id == land_id,
        models.Sensor.timestamp > datetime.utcnow() - timedelta(hours=24)
    ).order_by(desc(models.Sensor.timestamp)).limit(5).all()

    # Demo NDVI calculation (random 0-1; in prod, use ML on sensor data/satellite)
    ndvi = round(random.uniform(0.0, 1.0), 2)

    # Update land
    land.ndvi = ndvi
    land.is_degraded = ndvi < 0.3  # Threshold for degradation

    # Check for alert (degraded + low avg moisture <20 from recent sensors)
    if land.is_degraded and recent_sensors:
        avg_moisture = sum(s.moisture for s in recent_sensors) / len(recent_sensors)
        if avg_moisture < 20:
            # Create alert using models.Alert (DB model, not schemas.Alert)
            alert = models.Alert(
                message=f"Soil health declining in {land.name}: NDVI {ndvi}, avg moisture {avg_moisture:.1f}%. Initiate restoration.",
                land_id=land_id,
                severity="high" if avg_moisture < 15 else "medium"
            )
            db.add(alert)
            db.commit()

    db.commit()
    return ndvi

def scan_all_lands(db: Session):
    # Background task: Analyze all lands every 60s (demo; use scheduler in prod)
    lands = db.query(models.Land).all()
    for land in lands:
        analyze_land(db, land.id)