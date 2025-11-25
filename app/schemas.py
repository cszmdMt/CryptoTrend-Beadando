from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TransactionBase(BaseModel):
    amount: float
    price_at_transaction: float
    is_buy: bool = True

class TransactionCreate(TransactionBase):
    coin_id: int

class Transaction(TransactionBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True

class CoinBase(BaseModel):
    symbol: str
    name: str
    current_price: float
    market_cap: float

class CoinCreate(CoinBase):
    pass

class Coin(CoinBase):
    id: int
    transactions: List[Transaction] = []

    class Config:
        from_attributes = True