import subprocess
import time
import os
import sys

def main():
    print("🚀 CryptoTrend Rendszer Indítása...")
    print("-----------------------------------")

    # 1. Backend indítása külön folyamatban
    # A sys.executable biztosítja, hogy ugyanazt a Pythont használja (pl. venv)
    print("🔵 Backend indítása (FastAPI)...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"],
        env=os.environ.copy()
    )

    # Várunk pár másodpercet, hogy a szerver biztosan elinduljon
    time.sleep(3)

    # 2. Frontend indítása külön folyamatban
    print("🟠 Frontend indítása (Streamlit)...")
    frontend_process = subprocess.Popen(
        ["streamlit", "run", "frontend/app.py"],
        env=os.environ.copy()
    )

    print("-----------------------------------")
    print("✅ A rendszer fut!")
    print("Backend: http://127.0.0.1:8000")
    print("Frontend: http://localhost:8501")
    print("A leállításhoz nyomj CTRL+C-t a terminálban.")

    try:
        # Várakozás, amíg a folyamatok futnak
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Leállítás kezdeményezése...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Viszlát! 👋")

if __name__ == "__main__":
    main()