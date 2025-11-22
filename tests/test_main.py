from fastapi.testclient import TestClient
from app.main import app
from app.services import analysis
from app.schemas import Coin

# Ez a "kamu böngésző" a teszteléshez
client = TestClient(app)


# 1. TESZT: Működik a főoldal?
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "CryptoTrend API is running! 🚀"}


# 2. TESZT: Tudunk coint létrehozni? (Integrációs teszt)
def test_create_coin():
    # Egyedi nevet adunk neki, hogy ne ütközzön a DB-ben lévőkkel
    payload = {
        "symbol": "TESTCOIN",
        "name": "Test Coin",
        "current_price": 100.0,
        "market_cap": 50000.0
    }

    # Elküldjük a POST kérést
    response = client.post("/coins/", json=payload)

    # Ha már létezik, akkor 400-as hibát kapunk, de az is "sikeres" teszt,
    # mert azt jelenti, működik a validáció.
    if response.status_code == 400:
        assert response.json()["detail"] == "Coin already registered"
    else:
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "TESTCOIN"
        assert data["current_price"] == 100.0


# 3. TESZT: Funkcionális logika tesztelése (Unit test)
# Itt nem hívunk API-t, csak a matekot ellenőrizzük
def test_analysis_logic():
    # Csinálunk két kamu coint memóriában
    mock_coins = [
        Coin(id=1, symbol="A", name="Coin A", current_price=50.0, market_cap=1000, transactions=[]),
        Coin(id=2, symbol="B", name="Coin B", current_price=150.0, market_cap=2000, transactions=[])
    ]

    # Meghívjuk az elemzőt
    result = analysis.analyze_portfolio(mock_coins)

    # Ellenőrizzük a számokat
    assert result["total_coins"] == 2
    assert result["average_price"] == 100.0  # (50 + 150) / 2
    assert result["expensive_coins_count"] == 1  # Csak a 150-es nagyobb mint 100