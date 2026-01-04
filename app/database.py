import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. Betöltjük a .env fájlt (lokális fejlesztéshez)
load_dotenv()

# 2. Lekérjük az adatbázis URL-t a környezeti változókból.
# Ha nincs megadva (pl. lokálban vagyunk), akkor marad az SQLite alapértelmezettként.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crypto_trend.db")

# 3. Különleges javítás Render.com-hoz:
# A Render néha "postgres://"-el kezdi a címet, de a SQLAlchemy új verziói "postgresql://"-t várnak.
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 4. Beállítjuk a connect_args-ot
# A "check_same_thread" CSAK SQLite-nál kell, Postgres-nél hibát okoz!
connect_args = {}
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    connect_args = {"check_same_thread": False}

# 5. Létrehozzuk az engine-t a dinamikus beállításokkal
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()