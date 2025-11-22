from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.database import SessionLocal, engine

# --- ADATBÁZIS INDÍTÁSA ---
# Ez a sor a VARÁZSLAT! Létrehozza a táblákat (crypto_coins, transactions)
# az adatbázisban, ha még nem léteznek.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CryptoTrend API", version="1.0.0")

# --- Dependency (Függőség) ---
# Ez biztosítja, hogy minden kéréshez kapjunk egy adatbázis kapcsolatot,
# amit a kérés végén be is zárunk. Nagyon fontos az erőforrás-kezelés miatt!
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- VÉGPONTOK (ENDPOINTS) ---

@app.get("/")
def read_root():
    return {"message": "CryptoTrend API is running! 🚀"}

@app.post("/coins/", response_model=schemas.Coin)
def create_coin(coin: schemas.CoinCreate, db: Session = Depends(get_db)):
    """Új kriptovaluta felvétele a rendszerbe"""
    db_coin = crud.get_coin_by_symbol(db, symbol=coin.symbol)
    if db_coin:
        raise HTTPException(status_code=400, detail="Coin already registered")
    return crud.create_coin(db=db, coin=coin)

@app.get("/coins/", response_model=List[schemas.Coin])
def read_coins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Az összes elérhető coin listázása"""
    coins = crud.get_coins(db, skip=skip, limit=limit)
    return coins

@app.post("/coins/{coin_id}/transactions/", response_model=schemas.Transaction)
def create_transaction_for_coin(
    coin_id: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    """Vétel/Eladás rögzítése egy adott coinhoz"""
    # Kis trükk: a schemas.TransactionCreate-ben nincs coin_id (mert az URL-ből jön),
    # de a crud-nak szüksége van rá. Itt adjuk hozzá.
    transaction.coin_id = coin_id
    return crud.create_coin_transaction(db=db, transaction=transaction)