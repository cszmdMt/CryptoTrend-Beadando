import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- ALAPBEÁLLÍTÁSOK ---
# Ez mondja meg, hol érjük el a Backend szervert
API_URL = "http://127.0.0.1:8000"

# Az oldal címe és ikonja
st.set_page_config(page_title="CryptoTrend", page_icon="💸", layout="wide")

st.title("💸 CryptoTrend Dashboard")
st.markdown("Ez a felület kommunikál a Python Backenddel.")

# --- 1. OLDALSÁV: ÚJ ADAT FELVÉTELE ---
with st.sidebar:
    st.header("➕ Új Coin Hozzáadása")

    # Ez az űrlap (Form)
    with st.form("add_coin_form"):
        symbol = st.text_input("Rövidítés (pl. ETH)").upper()
        name = st.text_input("Teljes név (pl. Ethereum)")
        price = st.number_input("Ár ($)", min_value=0.01)
        market_cap = st.number_input("Market Cap ($)", min_value=0.0)

        submit_button = st.form_submit_button("Mentés az Adatbázisba")

        if submit_button:
            # Ha megnyomták a gombot, elküldjük az adatot a Backendnek
            payload = {
                "symbol": symbol,
                "name": name,
                "current_price": price,
                "market_cap": market_cap
            }

            try:
                # Itt történik a POST kérés a szerver felé
                response = requests.post(f"{API_URL}/coins/", json=payload)

                if response.status_code == 200:
                    st.success(f"Sikeres mentés: {name}!")
                else:
                    st.error(f"Hiba történt: {response.text}")
            except Exception as e:
                st.error(f"Nem sikerült elérni a szervert! {e}")

# --- 2. FŐRÉSZ: ADATOK MEGJELENÍTÉSE ---

# Lekérjük az összes coint a Backendtől (GET kérés)
try:
    response = requests.get(f"{API_URL}/coins/")
    if response.status_code == 200:
        coins = response.json()  # Átalakítjuk a választ Python listává
    else:
        st.error("Hiba az adatok lekérésekor.")
        coins = []
except:
    st.warning("⚠️ Nem érem el a Backend szervert. Fut az 'uvicorn'?")
    coins = []

# Ha van adatunk, akkor kirajzoljuk
if coins:
    # --- Felső sor: KPI Kártyák (Metrics) ---
    st.subheader("🔥 Kiemelt Árfolyamok")
    cols = st.columns(3)  # 3 oszlopra osztjuk a képernyőt

    # Csak az első 3 elemet tesszük ki kártyára
    for i, coin in enumerate(coins[:3]):
        with cols[i]:
            st.metric(
                label=coin['name'],
                value=f"${coin['current_price']:,.2f}",
                delta=None
            )

    st.divider()  # Választóvonal

    # --- Grafikon (Plotly) ---
    st.subheader("📊 Piaci Statisztika")

    # Pandas táblázattá alakítjuk az adatokat a könnyebb kezelésért
    df = pd.DataFrame(coins)

    # Oszlopdiagram készítése
    fig = px.bar(
        df,
        x="symbol",
        y="market_cap",
        title="Piaci Kapitalizáció (Market Cap)",
        color="symbol"  # Minden oszlop más színű legyen
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Részletes Táblázat ---
    st.subheader("📋 Részletes Lista")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Jelenleg üres az adatbázis. Vegyél fel új elemet bal oldalt! 👈")