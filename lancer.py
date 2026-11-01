# lancer.py - eppro
import os
import sys
import subprocess
import time

def check_and_install():
    try:
        import streamlit
        import pandas
        import openpyxl
        import plotly
    except ImportError:
        print("📦 Installation des dépendances eppro...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dépendances installées")

def kill_old():
    try:
        # Tue ancien streamlit si tourne déjà (Windows)
        os.system("taskkill /f /im streamlit.exe 2>nul")
    except:
        pass

def main():
    print("="*50)
    print("📱 eppro - Lancement en cours...")
    print("="*50)
    
    check_and_install()
    kill_old()

    # S'assure que pages/ existe
    if not os.path.exists("pages"):
        os.makedirs("pages")
        print("📁 Dossier pages/ créé")

    # Vérifie fichiers clés
    for f in ["dashboard_phone.py", "pages/Caisse.py", "pages/Inventaire.py"]:
        if not os.path.exists(f):
            print(f"⚠️ Manquant : {f}")
        else:
            print(f"✅ {f}")

    print("\n🚀 Lancement sur http://localhost:8501")
    print("Appuie sur CTRL+C pour arrêter\n")

    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "dashboard_phone.py",
            "--server.port", "8501",
            "--server.headless", "false",
            "--theme.primaryColor", "#0A1931",
            "--theme.backgroundColor", "#FFFFFF"
        ])
    except KeyboardInterrupt:
        print("\n👋 eppro arrêté")
        sys.exit(0)

if __name__ == "__main__":
    main()