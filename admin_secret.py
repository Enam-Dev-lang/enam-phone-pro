import streamlit as st
import json
import os
import datetime

FICHIER_CLES = "cles_valides.json"
st.set_page_config(page_title="ADMIN ENAM", layout="wide")
st.title("🔒 ADMIN SEULEMENT - Générateur de clés clients")

mdp = st.text_input("Mot de passe admin", type="password")
if mdp != "enam2026":
    st.stop()

# Charger clés existantes
if os.path.exists(FICHIER_CLES):
    with open(FICHIER_CLES, "r") as f:
        data = json.load(f)
        # Si ancien format liste simple, on convertit
        if isinstance(data, list) and len(data)>0 and isinstance(data[0], str):
            data = [{"id": i+1, "client": f"Client {i+1}", "telephone": "", "cle": c, "date": "", "statut": "actif"} for i,c in enumerate(data)]
else:
    data = []

st.write(f"Total clients: {len(data)}")

with st.form("nouveau_client"):
    st.subheader("Nouveau client")
    col1, col2 = st.columns(2)
    nom = col1.text_input("Nom boutique / Client")
    tel = col2.text_input("Téléphone WhatsApp")
    note = st.text_input("Note / Mise à jour particulière demandée")
    submit = st.form_submit_button("Générer Clé Numérotée")

    if submit:
        new_id = len(data) + 1
        new_cle = f"ENAM-{new_id:03d}-{nom.upper()[:4]}-2026"
        new_cle = new_cle.replace(" ", "")
        new_entry = {
            "id": new_id,
            "client": nom,
            "telephone": tel,
            "cle": new_cle,
            "date": datetime.datetime.now().strftime("%d/%m/%Y"),
            "note": note,
            "statut": "actif"
        }
        data.append(new_entry)
        with open(FICHIER_CLES, "w") as f:
            json.dump(data, f, indent=2)
        st.success(f"Clé créée pour {nom} : {new_cle}")
        st.info("N'oublie pas de faire git push pour qu'elle soit active en ligne !")

st.divider()
st.subheader("📋 Liste clients + clés")
st.dataframe(data, use_container_width=True)
