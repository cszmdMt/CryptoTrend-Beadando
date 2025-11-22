from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Fejlesztéshez egy egyszerű fájlt használunk adatbázisnak
SQLALCHEMY_DATABASE_URL = "sqlite:///./crypto_trend.db"

# A motor létrehozása (ez hajtja az adatbázist)
# A "check_same_thread": False csak SQLite-nál kell
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session létrehozása (ezen keresztül küldjük az adatokat)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ez az ŐS-osztály, ebből származtatjuk majd a tábláinkat
Base = declarative_base()