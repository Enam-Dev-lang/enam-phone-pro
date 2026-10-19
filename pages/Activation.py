import streamlit as st
import json, os
from datetime import datetime

st.set_page_config(page_title="Activation", layout="centered")
st.title("🔑 Activation")

FICHIER_ACTIVATION = "activation.json"
FICHIER_CLES = "cles_valides.json"

def is_activated():
    if not os.path.exists(FICHIER_ACTIVATION):
        return False
    try:
        with open(FICHIER_ACTIVATION, "r") as f:
            data = json.load(f)
            return "cle" in data
    except:
        return False

if is_activated():
    st.success("✅ Application déjà activée ! Merci pour votre achat.")
    with open(FICHIER_ACTIVATION, "r") as f:
        st.json(json.load(f))
    if st.button("Désactiver (test)"):
        os.remove(FICHIER_ACTIVATION)
        st.rerun()
    st.stop()

st.info("Entrez la clé reçue après paiement sur WhatsApp")

cle_saisie = st.text_input("Collez votre clé ici", placeholder="ENAM-XXXX-XXXX-XXXX").strip().upper()

if st.button("Activer maintenant", type="primary", use_container_width=True):
    if not os.path.exists(FICHIER_CLES):
        st.error("Fichier de clés introuvable. Contacte ENAM.")
        st.stop()
    
    with open(FICHIER_CLES, "r") as f:
        cles = json.load(f)
    
    # Vérifie si la clé existe
    valid = any(c["cle"] == cle_saisie for c in cles) if cles else False
    
    # Pour toi en test, on accepte aussi la clé MASTER
    if cle_saisie == "ENAM-MASTER-2026" or valid:
        with open(FICHIER_ACTIVATION, "w") as f:
            json.dump({"cle": cle_saisie, "date_activation": datetime.now().isoformat(), "app": "enam-phone-pro"}, f)
        st.success("🎉 Activation réussie ! Redémarre ton Dashboard.")
        st.balloons()
    else:
        st.error("❌ Clé invalide. Vérifie ou contacte 91 29 63 08 sur WhatsApp.")