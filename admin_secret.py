# admin_secret.py - A LANCER SEUL PAR TOI : streamlit run admin_secret.py
import streamlit as st, json, os, random, string
from datetime import datetime

KEYS_FILE = "keys_database.json"

def load_keys():
    if not os.path.exists(KEYS_FILE): return {}
    try:
        with open(KEYS_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {}

def save_keys(data):
    with open(KEYS_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=2, ensure_ascii=False)

def generate_key():
    # Format ENAM-XXXX-XXXX
    part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"ENAM-{part1}-{part2}"

st.set_page_config(page_title="ADMIN - Générateur de clés", layout="wide")
st.title("🔐 ADMIN - Générateur de clés à usage unique")
st.caption("Lance seulement en local : streamlit run admin_secret.py - Ne jamais envoyer ce fichier au client")

with st.form("gen"):
    client_name = st.text_input("Nom du client (ex: Boutique Koffi)")
    nb = st.number_input("Nombre de clés à générer", 1, 20, 1)
    if st.form_submit_button("Générer"):
        all_keys = load_keys()
        new_keys = []
        for _ in range(nb):
            k = generate_key()
            while k in all_keys:
                k = generate_key()
            all_keys[k] = {"client": client_name, "created_at": str(datetime.now()), "used": False, "used_at": ""}
            new_keys.append(k)
        save_keys(all_keys)
        st.success(f"{nb} clé(s) générée(s) pour {client_name}")
        for k in new_keys:
            st.code(k)

st.divider()
st.subheader("📋 Base de clés")
keys = load_keys()
if keys:
    import pandas as pd
    df = pd.DataFrame([
        {"Clé": k, "Client": v.get("client",""), "Créée": v.get("created_at","")[:19], "Utilisée": "✅ Oui" if v.get("used") else "❌ Non", "Utilisée le": v.get("used_at","")[:19]}
        for k,v in keys.items()
    ])
    st.dataframe(df, use_container_width=True)
    
    st.subheader("🗑️ Supprimer / Réactiver une clé")
    key_to_action = st.selectbox("Choisir clé", list(keys.keys()))
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Réactiver cette clé (la rendre réutilisable)"):
            keys[key_to_action]["used"] = False
            keys[key_to_action]["used_at"] = ""
            save_keys(keys)
            st.success(f"{key_to_action} réactivée")
            st.rerun()
    with col2:
        if st.button("Supprimer définitivement"):
            del keys[key_to_action]
            save_keys(keys)
            st.warning(f"{key_to_action} supprimée")
            st.rerun()
else:
    st.info("Aucune clé encore. Génère ta première clé au dessus.")
