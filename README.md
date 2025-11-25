# 💎 CryptoTrend - Multi-paradigmás Portfólió Kezelő

Ez a projekt az Eszterházy Károly Katolikus Egyetem "Multi paradigmás programozási nyelvek" kurzusának beadandó feladata. A rendszer egy modern, mikroszerviz-jellegű architektúrát valósít meg Python nyelven.

## 🚀 Funkciók és Technológiák

A projekt demonstrálja a három fő programozási paradigma szintézisét:

* **Objektumorientált (OOP):** SQLAlchemy adatbázis modellek, öröklődés (`BaseAsset` -> `CryptoCoin`), Pydantic sémák.
* **Funkcionális (FP):** Adattranszformáció és statisztikai elemzés `map`, `filter`, `reduce` és `lambda` kifejezésekkel (`services/analysis.py`).
* **Procedurális:** Adatgyűjtő szkript és API végpontok vezérlése.

**Tech Stack:**
* **Backend:** FastAPI, Uvicorn
* **Frontend:** Streamlit, Plotly
* **Adatbázis:** SQLite (SQLAlchemy ORM)
* **Külső API:** CoinGecko (Aszinkron hívásokkal)

## 🛠️ Telepítés és Indítás

A projekt futtatásához Python 3.10+ szükséges.

1. **Függőségek telepítése:**
   ```bash
   pip install -r requirements.txt