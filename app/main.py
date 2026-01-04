import logging
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.services import price_fetcher
from app.services import analysis

import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adatbázis táblák létrehozása
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="CryptoTrend API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    """
    Szerver indulásakor elindítjuk a háttérfolyamatot.
    Ez felel az AUTOMATIZÁLT adatfrissítésért.
    """
    asyncio.create_task(schedule_price_updates())


async def schedule_price_updates():
    """
    Végtelen ciklus, ami 10 percenként (600 mp) automatikusan
    frissíti a coinok árfolyamát a háttérben.
    """
    while True:
        logger.info("⏳ Háttérfolyamat: Automatikus árfrissítés indítása...")
        db = SessionLocal()
        try:
            # Meghívjuk a már megírt price_fetcher logikát
            await price_fetcher.update_prices(db)
        except Exception as e:
            logger.error(f"Hiba a háttérfolyamatban: {e}")
        finally:
            db.close()

        # Várunk 10 percet a következő futásig
        await asyncio.sleep(600)


def get_db():
    """
    Adatbázis kapcsolatot biztosító segédfüggvény.
    Minden kérés után automatikusan bezárja a kapcsolatot.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    """
    Alapértelmezett végpont az API elérhetőségének ellenőrzésére.
    """
    logger.info("Root végpont meghívva.")
    return {"message": "CryptoTrend API is running! 🚀"}


@app.post("/coins/", response_model=schemas.Coin)
def create_coin(coin: schemas.CoinCreate, db: Session = Depends(get_db)):
    """
    Új kriptovaluta felvétele az adatbázisba.
    Ellenőrzi, hogy létezik-e már a szimbólum.
    """
    db_coin = crud.get_coin_by_symbol(db, symbol=coin.symbol)
    if db_coin:
        logger.warning(f"Már létező coin hozzáadása megkísérelve: {coin.symbol}")
        raise HTTPException(status_code=400, detail="Coin already registered")

    logger.info(f"Új coin létrehozása: {coin.name}")
    return crud.create_coin(db=db, coin=coin)


@app.get("/coins/", response_model=List[schemas.Coin])
def read_coins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lekérdezi a rendszerben tárolt coinokat.
    Támogatja a lapozást (skip, limit).
    """
    coins = crud.get_coins(db, skip=skip, limit=limit)
    return coins

@app.get("/coins/{coin_id}", response_model=schemas.Coin)
def read_coin(coin_id: int, db: Session = Depends(get_db)):
    """
    Részletek végpont: Egy konkrét coin adatait adja vissza ID alapján.
    """
    db_coin = crud.get_coin(db, coin_id=coin_id)
    if db_coin is None:
        raise HTTPException(status_code=404, detail="Coin not found")
    return db_coin


@app.post("/coins/{coin_id}/transactions/", response_model=schemas.Transaction)
def create_transaction_for_coin(
        coin_id: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    """
    Tranzakció rögzítése egy adott coinhoz.
    """
    transaction.coin_id = coin_id
    logger.info(f"Tranzakció létrehozása a coin_id={coin_id}-hez.")
    return crud.create_coin_transaction(db=db, transaction=transaction)


@app.post("/refresh-prices/")
async def refresh_prices(db: Session = Depends(get_db)):
    """
    Aszinkron háttérfolyamat indítása:
    Lekéri az aktuális árakat a CoinGecko API-ról és frissíti az adatbázist.
    """
    logger.info("Árfolyam frissítés indítása...")
    return await price_fetcher.update_prices(db)


@app.get("/analytics/")
def get_analytics(db: Session = Depends(get_db)):
    """
    Statisztikai elemzés készítése a portfólióról.
    Funkcionális programozási eszközöket használ.
    """
    coins = crud.get_coins(db)
    # Átalakítás Pydantic modellre az elemzéshez
    pydantic_coins = [schemas.Coin.from_orm(c) for c in coins]
    return analysis.analyze_portfolio(pydantic_coins)


# Ez teszi lehetővé, hogy 'python main.py'-ként is futtatható legyen
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)