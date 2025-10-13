from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc  # For ordering if needed (optional)
from .. import crud, schemas, auth, models  # models for User type
from ..database import get_db
from typing import Optional, List

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/", response_model=List[schemas.Alert])
def read_alerts(
    current_user: Optional[models.User] = Depends(auth.get_current_user_optional),  # Optional auth to avoid 403
    land_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if current_user:
        user_lands = [land.id for land in crud.get_lands(db, current_user.id)]
        query = db.query(models.Alert).filter(
            models.Alert.resolved == False,
            models.Alert.land_id.in_(user_lands)
        )
        if land_id and land_id in user_lands:
            query = query.filter(models.Alert.land_id == land_id)
        return query.all()
    # Empty list if no user (demo tolerance)
    return []

@router.post("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    current_user: models.User = Depends(auth.get_current_user),  # Protected: Requires auth
    db: Session = Depends(get_db)
):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    land = db.query(models.Land).filter(models.Land.id == alert.land_id, models.Land.user_id == current_user.id).first()
    if not land:
        raise HTTPException(status_code=403, detail="Unauthorized")
    alert.resolved = True
    db.commit()
    db.refresh(alert)  # Optional: Refresh for latest state (consistency with create functions)
    return {"message": "Alert resolved"}