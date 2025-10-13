from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as SessionMaker
import os
from dotenv import load_dotenv
from .database import DATABASE_URL, get_db, engine, SessionLocal# Relative import for DB
from . import models  # Relative import for models
from .routes import users, lands, sensors, alerts  # Relative imports for routers
from .ai import scan_all_lands  # For background task
import asyncio

load_dotenv()  # Load .env for DATABASE_URL, JWT_SECRET

app = FastAPI(title="TerraSync API", description="Land Degradation Monitoring", version="1.0.0")

# CORS middleware for frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE
    allow_headers=["*"],  # Authorization, Content-Type
)

# Include routers
app.include_router(users.router, prefix="/api", tags=["users"])  # /api + /users = /api/users
app.include_router(lands.router, prefix="/api", tags=["lands"])  # /api + /lands = /api/lands
app.include_router(sensors.router, prefix="/api", tags=["sensors"])  # /api + /sensors = /api/sensors
app.include_router(alerts.router, prefix="/api", tags=["alerts"])  # /api + /alerts = /api/alerts

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "TerraSync API - Land Degradation Monitoring"}

# Startup event for background periodic scanning (analyze all lands every 60s)
# Startup event for background periodic scanning (analyze all lands every 60s)
# Startup event for background periodic scanning (analyze all lands every 60s)
@app.on_event("startup")
async def startup_event():
    async def periodic_scan():
        while True:
            db = None
            try:
                # Fixed: Use SessionLocal directly (no next(get_db()) misuse)
                SessionLocal = SessionMaker(autocommit=False, autoflush=False, bind=engine)
                db = SessionLocal()
                scan_all_lands(db)  # From ai.py
                await asyncio.sleep(60)  # Run every 60s (demo; adjust for prod)
            except Exception as e:
                print(f"Background scan error: {e}")
                await asyncio.sleep(60)  # Retry after error
            finally:
                if db:
                    db.close()  # Clean close, return to pool

    asyncio.create_task(periodic_scan())  # Start background task