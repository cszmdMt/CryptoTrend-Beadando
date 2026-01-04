# 💎 CryptoTrend Pro - Full Stack Kriptovaluta Elemző

**Eszterházy Károly Katolikus Egyetem — Multi paradigmás programozási nyelvek kurzus**

Ez a projekt egy többrétegű, modern webalkalmazás, amely valós idejű kriptovaluta piaci adatokat kezel, elemez és vizualizál. A rendszer demonstrálja a **FastAPI** (Backend) és a **Streamlit** (Frontend) integrációját, valamint a **Clean Architecture** elveit, miközben ötvözi a kurzuson tanult programozási paradigmákat.

## 🏗️ Architektúra és Technológiák

A rendszer moduláris felépítésű, szigorúan elválasztva a felelősségi köröket, demonstrálva a három fő paradigma szintézisét:

* **Backend (API Réteg):** `FastAPI` alapú REST API, `Uvicorn` szerverrel.
* **Adatbázis:** `SQLAlchemy` ORM (SQLite lokálisan, PostgreSQL élesben).
* **Frontend (UI Réteg):** `Streamlit` alapú interaktív dashboard `Plotly` diagramokkal.

### Programozási Paradigmák a Kódban:
* **Objektumorientált (OOP):** Adatbázis modellek öröklődéssel (`BaseAsset` -> `CryptoCoin` a `models.py`-ban) és Pydantic sémák.
* **Funkcionális (FP):** Adattranszformáció és statisztikai elemzés tisztán `map`, `filter`, `reduce` és `lambda` kifejezésekkel (`services/analysis.py`).
* **Procedurális:** Adatgyűjtő szkriptek, API végpontok vezérlése és az indító szkript (`run.py`).

---

## 🚀 Telepítés és Indítás (Lokálisan)

A projekt futtatásához **Python 3.10+** szükséges.

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