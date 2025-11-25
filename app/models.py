from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class BaseAsset(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CryptoCoin(BaseAsset):
    __tablename__ = "crypto_coins"

    current_price = Column(Float)
    market_cap = Column(Float)

    transactions = relationship("Transaction", back_populates="coin")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(Integer, ForeignKey("crypto_coins.id")) # Kapcsolat a coinnal

    amount = Column(Float)
    price_at_transaction = Column(Float)
    is_buy = Column(Boolean, default=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    coin = relationship("CryptoCoin", back_populates="transactions")