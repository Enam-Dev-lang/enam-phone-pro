import streamlit as st
import datetime
import json
import os
import base64

st.set_page_config(page_title="Facture ENAM", layout="centered")
st.title("🧾 Facture de Vente")

def get_logo_html():
    if os.path.exists("boutique_logo.png"):
        with open("boutique_logo.png", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            return f'<img src="data:image/png;base64,{data}" style="width:80px;height:80px;">'
    return '<div style="font-size:50px;">📱</div>'

if "boutique_nom" not in st.session_state:
    st.session_state.boutique_nom = "ENAM PHONE PRO"
    st.session_state.boutique_tel = "90 12 34 56"
    st.session_state.boutique_adresse = "Lome, Togo"

with st.expander("Configurer boutique + Logo", expanded=True):
    nom = st.text_input("Nom boutique", st.session_state.boutique_nom)
    tel = st.text_input("Tel boutique", st.session_state.boutique_tel)
    adresse = st.text_input("Adresse", st.session_state.boutique_adresse)
    logo_file = st.file_uploader("Upload LOGO", type=["png","jpg","jpeg"])
    if logo_file:
        with open("boutique_logo.png", "wb") as f:
            f.write(logo_file.getbuffer())
        st.image("boutique_logo.png", width=100)
    if st.button("Sauver"):
        st.session_state.boutique_nom = nom
        st.session_state.boutique_tel = tel
        st.session_state.boutique_adresse = adresse
        st.rerun()

st.divider()
client_nom = st.text_input("Client")
client_tel = st.text_input("Tel client")
agent = st.text_input("Agent vendeur")
date_fact = st.date_input("Date", value=datetime.date.today())

if not os.path.exists("factures.json"):
    num = 1
else:
    with open("factures.json", "r") as f:
        try:
            num = len(json.load(f)) + 1
        except:
            num = 1

code_facture = f"FAC-ENAM-{num:04d}-{datetime.date.today().year}"
st.info(f"Code Facture : {code_facture}")

if "lignes" not in st.session_state:
    st.session_state.lignes = [{"designation": "", "imei": "", "prix": 0, "qte": 1}]

for i, ligne in enumerate(st.session_state.lignes):
    c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
    with c1:
        ligne["designation"] = st.text_input(f"Designation {i+1}", value=ligne["designation"], key=f"des{i}")
    with c2:
        ligne["imei"] = st.text_input(f"IMEI {i+1}", value=ligne["imei"], key=f"imei{i}")
    with c3:
        ligne["prix"] = st.number_input(f"Prix {i+1}", value=ligne["prix"], key=f"prix{i}", step=1000)
    with c4:
        ligne["qte"] = st.number_input(f"Qte {i+1}", value=ligne["qte"], min_value=1, key=f"qte{i}")

if st.button("Ajouter telephone"):
    st.session_state.lignes.append({"designation": "", "imei": "", "prix": 0, "qte": 1})
    st.rerun()

total = sum(l["prix"] * l["qte"] for l in st.session_state.lignes)

st.divider()
st.subheader("Apercu Facture")
logo_html = get_logo_html()

html = f'<div style="border:2px solid #000; padding:20px; background:white; color:black; font-family:Arial;"><div style="display:flex; justify-content:space-between; border-bottom:2px solid #000; padding-bottom:10px;"><div style="display:flex; gap:15px; align-items:center;">{logo_html}<div><h2 style="margin:0;color:#0d47a1;">{st.session_state.boutique_nom}</h2><p>Tel: {st.session_state.boutique_tel} | {st.session_state.boutique_adresse}</p></div></div><div style="text-align:right;"><h3 style="color:red; margin:0;">FACTURE</h3><b>{code_facture}</b><br>{date_fact}</div></div><p><b>Client:</b> {client_nom} - {client_tel} <br><b>Agent:</b> {agent} | <b>Execute par:</b> {agent}</p><table style="width:100%; border-collapse:collapse;"><tr style="background:#0d47a1; color:white;"><th style="border:1px solid #000; padding:8px;">#</th><th style="border:1px solid #000; padding:8px;">Designation</th><th style="border:1px solid #000; padding:8px;">IMEI</th><th style="border:1px solid #000; padding:8px;">Qte</th><th style="border:1px solid #000; padding:8px;">Prix</th></tr>'

for idx, l in enumerate(st.session_state.lignes, 1):
    if l["designation"]:
        html += f'<tr><td style="border:1px solid #000; padding:8px;">{idx}</td><td style="border:1px solid #000; padding:8px;">{l["designation"]}</td><td style="border:1px solid #000; padding:8px;">{l["imei"]}</td><td style="border:1px solid #000; padding:8px; text-align:center;">{l["qte"]}</td><td style="border:1px solid #000; padding:8px; text-align:right;">{l["prix"]*l["qte"]:,} F</td></tr>'

html += f'<tr style="font-weight:bold; background:#f0f0f0;"><td colspan="4" style="border:1px solid #000; padding:8px; text-align:right;">TOTAL</td><td style="border:1px solid #000; padding:8px; text-align:right;">{total:,} F</td></tr></table><div style="display:flex; justify-content:space-between; margin-top:40px;"><div style="border-top:1px solid #000; width:40%; text-align:center;">Signature Client</div><div style="border-top:1px solid #000; width:40%; text-align:center;">Pour {st.session_state.boutique_nom}<br>Agent: {agent}</div></div></div>'

st.markdown(html, unsafe_allow_html=True)

if st.button("Enregistrer facture", type="primary", use_container_width=True):
    facture_data = {
        "code": code_facture,
        "date": str(date_fact),
        "client": client_nom,
        "client_tel": client_tel,
        "agent": agent,
        "boutique": st.session_state.boutique_nom,
        "lignes": st.session_state.lignes,
        "total": total
    }
    factures = []
    if os.path.exists("factures.json"):
        with open("factures.json", "r") as f:
            try:
                factures = json.load(f)
            except:
                factures = []
    factures.append(facture_data)
    with open("factures.json", "w") as f:
        json.dump(factures, f, indent=2, ensure_ascii=False)
    st.success(f"Facture {code_facture} enregistree !")
    st.balloons()