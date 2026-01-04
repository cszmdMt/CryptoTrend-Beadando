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
   

# 💎 CryptoTrend Pro - Full Stack Kriptovaluta Elemző

Ez a projekt egy többrétegű, modern webalkalmazás, amely valós idejű kriptovaluta piaci adatokat kezel, elemez és vizualizál. A rendszer demonstrálja a **FastAPI** (Backend) és a **Streamlit** (Frontend) integrációját, valamint a **Clean Architecture** elveit.

## 🏗️ Architektúra és Technológiák

A rendszer moduláris felépítésű, szigorúan elválasztva a felelősségi köröket:

* **Backend (API Réteg):** `FastAPI` alapú REST API.
    * **Adatbázis:** `SQLAlchemy` ORM (SQLite lokálisan, PostgreSQL élesben).
    * **Validáció:** `Pydantic` modellek.
    * **Aszinkronitás:** `asyncio` és `httpx` a háttérfolyamatokhoz.
* **Frontend (UI Réteg):** `Streamlit` alapú interaktív dashboard.
    * **Vizualizáció:** `Plotly` interaktív diagramok.
    * **Kommunikáció:** API hívások a backend felé.
* **Logika (Service Réteg):**
    * **OOP:** Objektumorientált adatmodellek (`models.py`).
    * **Funkcionális Programozás:** `map`, `filter`, `reduce` használata az elemzésekhez (`analysis.py`).

## 🚀 Telepítés és Indítás (Lokálisan)

A projekt futtatásához Python 3.9+ szükséges.

### 1. Környezet előkészítése
Hozd létre a virtuális környezetet és telepítsd a függőségeket:

```bash
# Virtuális környezet létrehozása
python -m venv venv

# Aktiválás (Windows)
venv\Scripts\activate

# Aktiválás (Mac/Linux)
source venv/bin/activate

# Csomagok telepítése
pip install -r requirements.txt