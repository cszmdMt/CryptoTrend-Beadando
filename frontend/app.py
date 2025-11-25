import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"
st.set_page_config(
    page_title="CryptoTrend Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    h1 {color: #4F8BF9;}
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 6])
with col1:
    # Internetes logó helyett egy sima emojit használunk, ha nincs neted, ne haljon le
    st.markdown("# 💎")
with col2:
    st.title("CryptoTrend Portfólió")
    st.caption("Multi-paradigmás Rendszer: FastAPI • SQLAlchemy • Streamlit")

with st.sidebar:
    st.header("⚙️ Vezérlőpult")

    st.subheader("🔄 Szinkronizáció")
    if st.button("🌍 Élő Árak Letöltése (Net)", type="primary"):
        with st.spinner("Kapcsolódás a tőzsdéhez..."):
            try:
                res = requests.post(f"{API_URL}/refresh-prices/")
                if res.status_code == 200:
                    st.success("✅ Árfolyamok frissítve!")
                    st.rerun()
                else:
                    st.error("Hiba a frissítésnél!")
            except Exception as e:
                st.error(f"Hálózati hiba: {e}")

    st.divider()

    with st.expander("➕ Új Eszköz Felvétele"):
        with st.form("add_coin_form"):
            symbol = st.text_input("Ticker (pl. SOL)").upper()
            name = st.text_input("Név (pl. Solana)")
            price = st.number_input("Ár ($)", min_value=0.01)
            market_cap = st.number_input("Market Cap ($)", min_value=0.0)

            if st.form_submit_button("Mentés"):
                payload = {"symbol": symbol, "name": name, "current_price": price, "market_cap": market_cap}
                try:
                    res = requests.post(f"{API_URL}/coins/", json=payload)
                    if res.status_code == 200:
                        st.success(f"✅ {name} mentve!")
                        st.rerun()
                    else:
                        st.error(f"Hiba: {res.text}")
                except Exception as e:
                    st.error("Szerver hiba!")

    st.info("💡 Tipp: Használd a fenti gombot az árak automatikus frissítéséhez.")

try:
    response = requests.get(f"{API_URL}/coins/")
    coins = response.json() if response.status_code == 200 else []
except:
    st.error("⚠️ A Backend szerver nem elérhető! Fut az 'uvicorn'?")
    coins = []


tab1, tab2, tab3 = st.tabs(["📈 Irányítópult", "🧠 Okos Elemzés", "📋 Adatbázis"])

with tab1:
    if coins:
        # KPI Kártyák (Top 4)
        st.subheader("🔥 Piaci Körkép")
        cols = st.columns(4)

        # Itt volt a hiba, most már javítva:
        for i, coin in enumerate(coins[:4]):
            with cols[i]:
                st.metric(
                    label=f"{coin['name']} ({coin['symbol']})",
                    value=f"${coin['current_price']:,.2f}",
                    delta="Élő adat"
                )

        st.markdown("---")

        st.subheader("📊 Portfólió Vizualizáció")
        df = pd.DataFrame(coins)

        g_col1, g_col2 = st.columns([2, 1])

        with g_col1:
            fig_bar = px.bar(
                df, x="symbol", y="market_cap", color="symbol",
                title="Piaci Érték (Market Cap)", template="plotly_white",
                labels={"market_cap": "USD", "symbol": "Token"}
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with g_col2:
            fig_pie = px.pie(
                df, values="current_price", names="symbol",
                title="Árfolyam Eloszlás", template="plotly_white",
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    else:
        st.warning("Nincs megjeleníthető adat. Vegyél fel coint a bal oldali menüben!")

with tab2:
    st.header("🧠 Intelligens Elemzés")
    st.markdown("Ez a modul **Funkcionális Programozási** eszközöket (`map`, `filter`, `reduce`) használ.")

    if st.button("Elemzés Futtatása ▶️"):
        try:
            stats_res = requests.get(f"{API_URL}/analytics/")
            if stats_res.status_code == 200:
                stats = stats_res.json()

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.info(f"**Coinok száma:** {stats.get('total_coins')} db")
                with c2:
                    st.success(f"**Átlagár:** ${stats.get('average_price'):,.2f}")
                with c3:
                    st.warning(f"**Legdrágább:** {stats.get('most_expensive')}")

                st.write("### 💎 Prémium Coinok (>100$)")
                st.json(stats.get("expensive_coins_list"))
            else:
                st.error("Hiba az elemzésnél.")
        except Exception as e:
            st.error(f"Hiba: {e}")

with tab3:
    st.subheader("📋 Teljes Adatbázis Tartalom")
    if coins:
        df = pd.DataFrame(coins)
        st.dataframe(
            df[["id", "name", "symbol", "current_price", "market_cap"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "current_price": st.column_config.NumberColumn("Ár", format="$%.2f"),
                "market_cap": st.column_config.NumberColumn("Market Cap", format="$%.2f"),
                "symbol": "Ticker"
            }
        )
    else:
        st.info("Az adatbázis üres.")