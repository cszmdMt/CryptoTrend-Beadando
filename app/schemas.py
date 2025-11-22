from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Pydantic Modellek (Data Transfer Objects) ---

# 1. Tranzakció Schemák
# Ez az alap, amit mindenki lát
class TransactionBase(BaseModel):
    amount: float
    price_at_transaction: float
    is_buy: bool = True

# Ezt használjuk, amikor LÉTREHOZUNK egy tranzakciót (kell a coin_id)
class TransactionCreate(TransactionBase):
    coin_id: int

# Ezt küldjük VISSZA a kliensnek (itt már van ID és időbélyeg is)
class Transaction(TransactionBase):
    id: int
    timestamp: datetime

    # Ez a varázslat: engedi, hogy az ORM objektumot (SQLAlchemy)
    # Pydantic modellé alakítsuk.
    class Config:
        from_attributes = True

# 2. Kriptovaluta Schemák
class CoinBase(BaseModel):
    symbol: str
    name: str
    current_price: float
    market_cap: float

# Létrehozásnál (ugyanaz, mint az alap)
class CoinCreate(CoinBase):
    pass

# Válasznál (visszaküldjük a hozzá tartozó tranzakciókat is!)
class Coin(CoinBase):
    id: int
    # Itt ágyazzuk be a tranzakciók listáját
    transactions: List[Transaction] = []

    class Config:
        from_attributes = True