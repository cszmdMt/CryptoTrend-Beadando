from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# --- OOP PARADIGMA: ÖRÖKLŐDÉS (Inheritance) ---
# Létrehozunk egy absztrakt "BaseAsset" osztályt.
# Ebből nem lesz tábla, de a közös tulajdonságokat (id, symbol, name)
# innen örökli majd minden eszköz (pl. Kripto, Részvény).
class BaseAsset(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True) # pl. BTC
    name = Column(String)                            # pl. Bitcoin
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Ez a konkrét tábla a Kriptovalutáknak
# Látod? A (BaseAsset)-ből öröklődik!
class CryptoCoin(BaseAsset):
    __tablename__ = "crypto_coins"

    current_price = Column(Float)  # Jelenlegi ár USD-ben
    market_cap = Column(Float)     # Piaci méret

    # Kapcsolat: Egy coinhoz sok tranzakció tartozhat
    transactions = relationship("Transaction", back_populates="coin")

# Tranzakciók tábla (Vétel/Eladás naplózása)
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(Integer, ForeignKey("crypto_coins.id")) # Kapcsolat a coinnal

    amount = Column(Float)         # Mennyiség (pl. 0.5)
    price_at_transaction = Column(Float) # Árfolyam vásárláskor
    is_buy = Column(Boolean, default=True) # True = Vétel, False = Eladás
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Visszafelé mutató kapcsolat
    coin = relationship("CryptoCoin", back_populates="transactions")