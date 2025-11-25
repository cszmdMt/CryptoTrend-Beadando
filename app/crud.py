from sqlalchemy.orm import Session
from app import models, schemas


def get_coin(db: Session, coin_id: int):
    return db.query(models.CryptoCoin).filter(models.CryptoCoin.id == coin_id).first()

def get_coin_by_symbol(db: Session, symbol: str):
    return db.query(models.CryptoCoin).filter(models.CryptoCoin.symbol == symbol).first()

def get_coins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CryptoCoin).offset(skip).limit(limit).all()

def create_coin(db: Session, coin: schemas.CoinCreate):
    db_coin = models.CryptoCoin(
        symbol=coin.symbol,
        name=coin.name,
        current_price=coin.current_price,
        market_cap=coin.market_cap
    )
    db.add(db_coin)
    db.commit()
    db.refresh(db_coin)
    return db_coin


def create_coin_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_coin_price(db: Session, symbol: str, new_price: float):
    db_coin = get_coin_by_symbol(db, symbol)
    if db_coin:
        db_coin.current_price = new_price
        db.commit()
        db.refresh(db_coin)
    return db_coin