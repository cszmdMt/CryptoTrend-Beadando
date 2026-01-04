from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class BaseAsset(Base):
    """
        Absztrakt ősosztály, amely a közös tulajdonságokat tartalmazza (pl. id, név, létrehozás ideje).
        Ebből származik le minden konkrét pénzügyi eszköz modellje.
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CryptoCoin(BaseAsset):
    """
        Kriptovaluták adatait tároló adatbázis modell.
        Örökli a BaseAsset mezőit, és kiegészíti árfolyam adatokkal.
    """
    __tablename__ = "crypto_coins"

    current_price = Column(Float)
    market_cap = Column(Float)

    transactions = relationship("Transaction", back_populates="coin")

class Transaction(Base):
    """
        Egy adott coinhoz tartozó tranzakció (vétel/eladás) modellje.
        Tárolja a mennyiséget, árat és a tranzakció idejét.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(Integer, ForeignKey("crypto_coins.id")) # Kapcsolat a coinnal

    amount = Column(Float)
    price_at_transaction = Column(Float)
    is_buy = Column(Boolean, default=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    coin = relationship("CryptoCoin", back_populates="transactions")