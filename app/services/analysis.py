from functools import reduce
from typing import List
from app.schemas import Coin


def analyze_portfolio(coins: List[Coin]):
    """
        Portfólió elemzése funkcionális programozási eszközökkel.

        A függvény tisztán funkcionális megközelítést alkalmaz:
        - map: Adattranszformációhoz
        - filter: Szűréshez
        - reduce: Aggregációhoz (összegzés)

        :param coins: A coin objektumok listája
        :return: Szótár (dict) a számított statisztikákkal
    """

    if not coins:
        return {"message": "Nincs elég adat az elemzéshez."}

    # 1. MAP & LAMBDA: Kinyerjük csak az árakat egy listába
    # (Átalakítjuk a Coin objektumokat float számokká)
    prices = list(map(lambda c: c.current_price, coins))

    # 2. FILTER: Megkeressük a "Nagyágyúkat" (amik drágábbak, mint $100)
    expensive_coins = list(filter(lambda c: c.current_price > 100, coins))
    expensive_names = list(map(lambda c: c.name, expensive_coins))

    # 3. REDUCE: Kiszámoljuk az összes coin átlagárát
    # (Összeadjuk az árakat, majd elosztjuk a darabszámmal)
    total_price_sum = reduce(lambda a, b: a + b, prices)
    average_price = total_price_sum / len(coins)

    return {
        "total_coins": len(coins),
        "average_price": round(average_price, 2),
        "expensive_coins_count": len(expensive_coins),
        "expensive_coins_list": expensive_names,
        "most_expensive": max(coins, key=lambda c: c.current_price).name
    }