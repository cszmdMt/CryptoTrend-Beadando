import httpx
from sqlalchemy.orm import Session
from app import crud

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
        return {"message": "Nincs coin az adatbázisban, amit frissíteni lehetne."}

    # 2. Összegyűjtjük a szimbólumokat (pl. bitcoin, ethereum)
    # A CoinGecko a teljes nevet (name) szereti kisbetűvel, nem a szimbólumot!
    coin_ids = [coin.name.lower() for coin in coins]
    ids_string = ",".join(coin_ids)  # pl. "bitcoin,ethereum,solana"

    # 3. Kimegyünk a netre (aszinkron hívás!)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                COINGECKO_API_URL,
                params={"ids": ids_string, "vs_currencies": "usd"}
            )
            data = response.json()
        except Exception as e:
            print(f"Hiba a letöltéskor: {e}")
            return {"error": "Nem sikerült elérni a CoinGecko-t"}

    # 4. Frissítjük az adatbázist a kapott adatokkal
    updated_count = 0
    for coin in coins:
        # A coin neve kisbetűvel a kulcs (pl. "bitcoin")
        coin_key = coin.name.lower()

        if coin_key in data:
            new_price = data[coin_key]["usd"]
            # Itt hívjuk meg a CRUD update függvényét
            crud.update_coin_price(db, coin.symbol, new_price)
            updated_count += 1

    return {"message": f"Sikeresen frissítve {updated_count} db coin ára!"}