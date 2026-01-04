from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TransactionBase(BaseModel):
    """
        A tranzakciók alapvető adatait tartalmaző Pydantic séma.
    """
    amount: float
    price_at_transaction: float
    is_buy: bool = True

class TransactionCreate(TransactionBase):
    """
        Tranzakció létrehozásakor használt séma (validációhoz)
    """
    coin_id: int

class Transaction(TransactionBase):
    """
        A tranzakciók lekérdezésekor visszaadott teljes adatmodell
    """
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True

class CoinBase(BaseModel):
    """
        A coinok alapvető adatait tartalmazó Pydantic séma.
    """
    symbol: str
    name: str
    current_price: float
    market_cap: float

class CoinCreate(CoinBase):
    """
        Új Coin hozzáadásakor használt séma.
    """
    pass

class Coin(CoinBase):
    """
        A coinok lekérdezésekor visszaadott teljes adatmodell.
        Tartalmazza a hozzá tartozó tranzakciók listáját is.
    """
    id: int
    transactions: List[Transaction] = []

    class Config:
        from_attributes = True