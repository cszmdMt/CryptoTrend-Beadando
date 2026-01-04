import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import analysis
from app.schemas import Coin

client = TestClient(app)


def test_read_main():
    """
    Alapvető API elérhetőség tesztelése.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "CryptoTrend API is running! 🚀"}


def test_create_coin():
    """
    Coin létrehozás tesztelése.
    Mivel adatbázist használ, előfordulhat, hogy másodjára 400-at ad,
    ezért kezeljük mindkét esetet, hogy a teszt stabil maradjon.
    """
    payload = {
        "symbol": "TESTCOIN",
        "name": "Test Coin",
        "current_price": 100.0,
        "market_cap": 50000.0
    }

    response = client.post("/coins/", json=payload)

    if response.status_code == 400:
        assert response.json()["detail"] == "Coin already registered"
    else:
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "TESTCOIN"
        assert data["current_price"] == 100.0


# ITT A JAVÍTÁS: Paraméterezett teszt használata
@pytest.mark.parametrize("price1, price2, expected_avg, expected_expensive_count", [
    (50.0, 150.0, 100.0, 1),   # 1. Eset: Egy olcsó (<100), egy drága (>100) -> Átlag 100
    (10.0, 20.0, 15.0, 0),     # 2. Eset: Csak olcsók -> 0 drága
    (200.0, 400.0, 300.0, 2),  # 3. Eset: Csak drágák -> 2 drága
])
def test_analysis_parametrized(price1, price2, expected_avg, expected_expensive_count):
    """
    Az elemző logika tesztelése több bemeneti kombinációval (parametrize).
    Ez ellenőrzi, hogy a map/filter/reduce logika jól számol-e.
    """
    mock_coins = [
        Coin(id=1, symbol="A", name="Coin A", current_price=price1, market_cap=1000, transactions=[]),
        Coin(id=2, symbol="B", name="B", current_price=price2, market_cap=2000, transactions=[])
    ]

    result = analysis.analyze_portfolio(mock_coins)

    assert result["total_coins"] == 2
    assert result["average_price"] == expected_avg
    assert result["expensive_coins_count"] == expected_expensive_count