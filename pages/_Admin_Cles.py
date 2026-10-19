import streamlit as st
import json, os, random, string
from datetime import datetime

st.set_page_config(page_title="Admin Clés", layout="centered")
st.title("🔐 ADMIN - Générateur de clés")

# MOT DE PASSE ADMIN - CHANGE LE
PASSWORD_ADMIN = "enam2026"

pwd = st.text_input("Mot de passe Admin", type="password")
if pwd != PASSWORD_ADMIN:
    st.warning("Accès réservé à ENAM")
    st.stop()

st.success("Connecté en Admin")

FICHIER_CLES = "cles_valides.json"

if not os.path.exists(FICHIER_CLES):
    with open(FICHIER_CLES, "w") as f:
        json.dump([], f)

nom_client = st.text_input("Nom du client")
tel_client = st.text_input("Téléphone / WhatsApp")

def generer_cle():
    part = lambda: ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"ENAM-{part()}-{part()}-{part()}"

if st.button("GÉNÉRER UNE CLÉ", type="primary"):
    if not nom_client:
        st.error("Mets le nom du client")
    else:
        nouvelle_cle = generer_cle()
        with open(FICHIER_CLES, "r") as f:
            cles = json.load(f)
        cles.append({"cle": nouvelle_cle, "client": nom_client, "tel": tel_client, "date": datetime.now().isoformat()})
        with open(FICHIER_CLES, "w") as f:
            json.dump(cles, f, indent=2)
        st.success(f"Clé pour {nom_client} :")
        st.code(nouvelle_cle)
        st.info("Copie cette clé et envoie-la au client. N'oublie pas de faire git push pour que la clé soit active sur internet.")

st.divider()
st.subheader("Toutes les clés générées")
with open(FICHIER_CLES, "r") as f:
    st.json(json.load(f))