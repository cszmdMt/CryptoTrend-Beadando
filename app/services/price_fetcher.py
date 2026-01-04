import httpx
import logging
from sqlalchemy.orm import Session
from app import crud

# Beállítjuk a loggert
logger = logging.getLogger(__name__)

# Ez a CoinGecko API címe (ingyenes)
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"


async def update_prices(db: Session):
    """
    Ez a függvény végigmegy az adatbázisban lévő coinokon,
    lekérdezi az aktuális árukat a netről, és frissíti őket.
    """
    # 1. Lekérjük az összes coint az adatbázisból
    coins = crud.get_coins(db)

    if not coins:
        logger.warning("Nincs coin az adatbázisban, amit frissíteni lehetne.")
        return {"message": "Nincs coin az adatbázisban, amit frissíteni lehetne."}

    # 2. Összegyűjtjük a szimbólumokat (pl. bitcoin, ethereum)
    coin_ids = [coin.name.lower() for coin in coins]
    ids_string = ",".join(coin_ids)

    # 3. Kimegyünk a netre (aszinkron hívás!)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                COINGECKO_API_URL,
                params={"ids": ids_string, "vs_currencies": "usd"}
            )
            response.raise_for_status() # Hiba dobása, ha nem 200 OK a válasz
            data = response.json()
        except Exception as e:
            # ITT a javítás: print helyett logger.error
            logger.error(f"Hiba a letöltéskor: {e}")
            return {"error": "Nem sikerült elérni a CoinGecko-t"}

    # 4. Frissítjük az adatbázist a kapott adatokkal
    updated_count = 0
    for coin in coins:
        coin_key = coin.name.lower()

        if coin_key in data:
            new_price = data[coin_key]["usd"]
            crud.update_coin_price(db, coin.symbol, new_price)
            updated_count += 1

    logger.info(f"Sikeresen frissítve {updated_count} db coin ára!")
    return {"message": f"Sikeresen frissítve {updated_count} db coin ára!"}