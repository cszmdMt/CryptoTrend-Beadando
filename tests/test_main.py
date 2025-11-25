from fastapi.testclient import TestClient
from app.main import app
from app.services import analysis
from app.schemas import Coin

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "CryptoTrend API is running! 🚀"}


def test_create_coin():
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


def test_analysis_logic():
    mock_coins = [
        Coin(id=1, symbol="A", name="Coin A", current_price=50.0, market_cap=1000, transactions=[]),
        Coin(id=2, symbol="B", name="Coin B", current_price=150.0, market_cap=2000, transactions=[])
    ]

    result = analysis.analyze_portfolio(mock_coins)

    assert result["total_coins"] == 2
    assert result["average_price"] == 100.0
    assert result["expensive_coins_count"] == 1