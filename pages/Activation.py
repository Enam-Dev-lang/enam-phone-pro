import streamlit as st
import json
import os

FICHIER_CLES = "cles_valides.json"
FICHIER_LICENCE = "licence.json"

st.set_page_config(page_title="Activation ENAM", layout="centered")
st.title("🔑 Activation de votre licence")
st.info("Entrez la clé reçue après paiement sur WhatsApp")

cle_saisie = st.text_input("Collez votre clé ici", placeholder="ENAM-001-... ou ENAM-MASTER-2026")

if st.button("Activer maintenant", type="primary", use_container_width=True):
    if not cle_saisie.strip():
        st.warning("Veuillez coller une clé")
        st.stop()

    if not os.path.exists(FICHIER_CLES):
        st.error("Fichier de clés introuvable. Contacte ENAM.")
        st.stop()

    with open(FICHIER_CLES, "r") as f:
        try:
            cles_data = json.load(f)
        except:
            cles_data = []

    # Support ancien format (liste de string) et nouveau format (liste de dict avec numérotation)
    valides = []
    for item in cles_data:
        if isinstance(item, dict):
            valides.append(item.get("cle", ""))
        else:
            valides.append(item)

    cle_clean = cle_saisie.strip()

    # Master + clés clients numérotées ENAM-001 etc
    if cle_clean == "ENAM-MASTER-2026" or cle_clean in valides:
        with open(FICHIER_LICENCE, "w") as f:
            json.dump({"active": True, "cle": cle_clean, "date": "2026"}, f)
        st.success("✅ Activation réussie ! Va dans Dashboard maintenant")
        st.balloons()
    else:
        st.error("❌ Clé invalide. Vérifie bien ou contacte ENAM sur WhatsApp")

st.divider()
st.caption("Si tu es l'admin, lance en local : streamlit run admin_secret.py pour générer les clés ENAM-001, ENAM-002...")