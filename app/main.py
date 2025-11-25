from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.services import price_fetcher
from app.services import analysis

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CryptoTrend API", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "CryptoTrend API is running! 🚀"}

@app.post("/coins/", response_model=schemas.Coin)
def create_coin(coin: schemas.CoinCreate, db: Session = Depends(get_db)):
    db_coin = crud.get_coin_by_symbol(db, symbol=coin.symbol)
    if db_coin:
        raise HTTPException(status_code=400, detail="Coin already registered")
    return crud.create_coin(db=db, coin=coin)

@app.get("/coins/", response_model=List[schemas.Coin])
def read_coins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    coins = crud.get_coins(db, skip=skip, limit=limit)
    return coins

@app.post("/coins/{coin_id}/transactions/", response_model=schemas.Transaction)
def create_transaction_for_coin(
    coin_id: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    transaction.coin_id = coin_id
    return crud.create_coin_transaction(db=db, transaction=transaction)


@app.post("/refresh-prices/")
async def refresh_prices(db: Session = Depends(get_db)):
    return await price_fetcher.update_prices(db)

@app.get("/analytics/")
def get_analytics(db: Session = Depends(get_db)):
    coins = crud.get_coins(db)
    pydantic_coins = [schemas.Coin.from_orm(c) for c in coins]
    return analysis.analyze_portfolio(pydantic_coins)