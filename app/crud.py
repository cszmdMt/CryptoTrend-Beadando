from sqlalchemy.orm import Session
from app import models, schemas

# --- Kriptovaluta Műveletek (READ & CREATE) ---

def get_coin(db: Session, coin_id: int):
    """Egyetlen coin lekérése ID alapján"""
    return db.query(models.CryptoCoin).filter(models.CryptoCoin.id == coin_id).first()

def get_coin_by_symbol(db: Session, symbol: str):
    """Coin keresése szimbólum (pl. BTC) alapján"""
    return db.query(models.CryptoCoin).filter(models.CryptoCoin.symbol == symbol).first()

def get_coins(db: Session, skip: int = 0, limit: int = 100):
    """Az összes coin listázása (lapozhatóan)"""
    return db.query(models.CryptoCoin).offset(skip).limit(limit).all()

def create_coin(db: Session, coin: schemas.CoinCreate):
    """Új coin létrehozása az adatbázisban"""
    # Itt alakítjuk át a Pydantic sémát SQLAlchemy modellé
    db_coin = models.CryptoCoin(
        symbol=coin.symbol,
        name=coin.name,
        current_price=coin.current_price,
        market_cap=coin.market_cap
    )
    db.add(db_coin)
    db.commit()      # Véglegesítjük a mentést
    db.refresh(db_coin) # Frissítjük az objektumot (hogy megkapjuk az ID-t)
    return db_coin

# --- Tranzakció Műveletek (CREATE) ---

def create_coin_transaction(db: Session, transaction: schemas.TransactionCreate):
    """Új tranzakció rögzítése egy coinhoz"""
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# --- Frissítés (UPDATE) ---

def update_coin_price(db: Session, symbol: str, new_price: float):
    """Árfolyam frissítése (ezt használja majd a háttérfolyamat)"""
    db_coin = get_coin_by_symbol(db, symbol)
    if db_coin:
        db_coin.current_price = new_price
        db.commit()
        db.refresh(db_coin)
    return db_coin