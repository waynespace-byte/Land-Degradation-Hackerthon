from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import pymysql  # For MySQL support
pymysql.install_as_MySQLdb()  # Shim: Enables SQLAlchemy to use pymysql as MySQL driver
from .models import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/terasync_db")  # Updated: MySQL default
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()