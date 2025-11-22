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

    st.divider()
    st.header("🔄 Árak Frissítése")
    if st.button("Élő Árfolyamok Letöltése (Net)"):
        with st.spinner("Kapcsolódás a CoinGecko-hoz..."):
            try:
                res = requests.post(f"{API_URL}/refresh-prices/")
                if res.status_code == 200:
                    st.success(res.json().get("message"))
                    st.rerun()  # Újratölti az oldalt a friss adatokkal
                else:
                    st.error("Hiba a frissítésnél!")
            except Exception as e:
                st.error(f"Hálózati hiba: {e}")

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

    st.divider()
    st.subheader("🧠 Intelligens Elemzés (Funkcionális Programozás)")

    try:
        # Lekérjük az elemzést a backendtől
        stats_res = requests.get(f"{API_URL}/analytics/")
        if stats_res.status_code == 200:
            stats = stats_res.json()

            # Kirakjuk 4 oszlopba a számokat
            s1, s2, s3, s4 = st.columns(4)
            s1.metric("Coinok száma", stats.get("total_coins"))
            s2.metric("Átlagár ($)", stats.get("average_price"))
            s3.metric("100$ felettiek", stats.get("expensive_coins_count"))
            s4.metric("Legdrágább", stats.get("most_expensive"))

            # Egy kis extra infó
            with st.expander("Kik a nagyágyúk? (>100$)"):
                st.write(", ".join(stats.get("expensive_coins_list", [])))

        else:
            st.info("Nincs elég adat az elemzéshez.")
    except Exception as e:
        st.error(f"Hiba az elemzés betöltésekor: {e}")

    # --- Részletes Táblázat ---
    st.subheader("📋 Részletes Lista")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Jelenleg üres az adatbázis. Vegyél fel új elemet bal oldalt! 👈")