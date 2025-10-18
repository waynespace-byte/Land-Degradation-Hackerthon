from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas, auth, ai, models  # Relative imports
from ..database import get_db

router = APIRouter(prefix="/lands", tags=["lands"])

@router.post("/", response_model=schemas.Land)
def create_land(land: schemas.LandCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Create full Land model with server-side user_id
    db_land = models.Land(  # Changed: db_land to avoid overwriting parameter 'land'
        name=land.name,
        location=land.location,
        user_id=current_user.id  # Set from authenticated user
    )
    return crud.create_land(db=db, land=db_land)

@router.get("", response_model=List[schemas.Land])
def read_lands(current_user: Optional[models.User] = Depends(auth.get_current_user_optional), db: Session = Depends(get_db)):
    user_id = current_user.id if current_user else None
    return crud.get_lands(db, user_id=user_id)

@router.post("/{land_id}/analyze", response_model=dict)  # Added: response_model for clarity (dict for {"ndvi": ..., "degraded": ...})
def analyze_ndvi(land_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    land = db.query(models.Land).filter(models.Land.id == land_id, models.Land.user_id == current_user.id).first()
    if not land:
        raise HTTPException(status_code=403, detail="Unauthorized")
    ndvi = ai.analyze_land(db, land_id)
    db.refresh(land)  # Optional: Refresh land for latest is_degraded after ai.update
    return {"ndvi": ndvi, "degraded": land.is_degraded}

# ADD THIS NEW ENDPOINT HERE (after analyze_ndvi, before end of file)
@router.get("/{land_id}", response_model=schemas.Land)
def read_land(land_id: int, current_user: Optional[models.User] = Depends(auth.get_current_user_optional), db: Session = Depends(get_db)):
    if current_user:
        land = db.query(models.Land).filter(models.Land.id == land_id, models.Land.user_id == current_user.id).first()
        if not land:
            raise HTTPException(status_code=403, detail="Unauthorized")
        return land
    # Public read if no auth (demo tolerance)
    land = db.query(models.Land).filter(models.Land.id == land_id).first()
    if not land:
        raise HTTPException(status_code=404, detail="Land not found")
    return land