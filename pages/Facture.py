import streamlit as st
import datetime
import json
import os
import base64

st.set_page_config(page_title="Facture ENAM PRO", layout="centered")

def get_logo_base64():
    if os.path.exists("boutique_logo.png"):
        with open("boutique_logo.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# --- CONFIG ---
if "boutique_nom" not in st.session_state:
    st.session_state.boutique_nom = "ENAM PHONE PRO"
    st.session_state.boutique_tel = "90 12 34 56"
    st.session_state.boutique_adresse = "Lomé, Togo - Grand Marché"
    st.session_state.boutique_email = "contact@enamphone.tg"

st.title("🧾 Facture PRO")

with st.expander("⚙️ Configuration Boutique", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        nom = st.text_input("Nom boutique", st.session_state.boutique_nom)
        tel = st.text_input("Téléphone", st.session_state.boutique_tel)
        adresse = st.text_input("Adresse", st.session_state.boutique_adresse)
    with c2:
        email = st.text_input("Email", st.session_state.boutique_email)
        logo_file = st.file_uploader("Logo boutique (PNG/JPG)", type=["png","jpg","jpeg"])
        if logo_file:
            with open("boutique_logo.png", "wb") as f:
                f.write(logo_file.getbuffer())
            st.success("Logo ajouté")
    if st.button("Sauvegarder"):
        st.session_state.boutique_nom = nom
        st.session_state.boutique_tel = tel
        st.session_state.boutique_adresse = adresse
        st.session_state.boutique_email = email
        st.rerun()

# --- INFOS ---
st.divider()
col1, col2 = st.columns(2)
with col1:
    client_nom = st.text_input("Nom Client", placeholder="Ex: M. Kodjo Agbé")
    client_tel = st.text_input("Tél Client", placeholder="Ex: 90 12 34 56")
with col2:
    agent = st.text_input("Vendeur / Agent", placeholder="Ex: Paul")
    date_fact = st.date_input("Date", datetime.date.today())

# Numero
if os.path.exists("factures.json"):
    try:
        with open("factures.json","r") as f:
            num = len(json.load(f)) + 1
    except:
        num = 1
else:
    num = 1

code_facture = f"FAC-{datetime.date.today().year}-{num:04d}"
st.caption(f"Code facture: **{code_facture}** | Place pour logo: client ajoute son logo lui-même")

# --- ARTICLES ---
st.subheader("Articles")
if "lignes" not in st.session_state:
    st.session_state.lignes = [{"designation": "iPhone 13 128Go Noir", "imei": "", "prix": 250000, "qte": 1}]

for i, l in enumerate(st.session_state.lignes):
    c1, c2, c3, c4 = st.columns([3,2,2,1])
    with c1:
        l["designation"] = st.text_input(f"Désignation {i+1}", l["designation"], key=f"d{i}", label_visibility="collapsed", placeholder="Désignation")
    with c2:
        l["imei"] = st.text_input(f"IMEI {i+1}", l["imei"], key=f"im{i}", label_visibility="collapsed", placeholder="IMEI")
    with c3:
        l["prix"] = st.number_input(f"Prix {i+1}", value=l["prix"], key=f"p{i}", label_visibility="collapsed", step=1000)
    with c4:
        l["qte"] = st.number_input(f"Qté", value=l["qte"], min_value=1, key=f"q{i}", label_visibility="collapsed")

cc1, cc2 = st.columns(2)
with cc1:
    if st.button("➕ Ajouter article"):
        st.session_state.lignes.append({"designation": "", "imei": "", "prix": 0, "qte": 1})
        st.rerun()
with cc2:
    if st.button("🗑️ Vider"):
        st.session_state.lignes = [{"designation": "", "imei": "", "prix": 0, "qte": 1}]
        st.rerun()

total = sum(l["prix"]*l["qte"] for l in st.session_state.lignes)

# --- APERCU PRO ---
st.divider()
st.subheader("Aperçu Expert - Prêt à imprimer")

logo_b64 = get_logo_base64()
if logo_b64:
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:85px; height:85px; object-fit:contain; border-radius:12px; background:white; padding:5px;">'
else:
    logo_html = f'<div style="width:85px; height:85px; border:2px dashed #6366f1; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#6366f1; font-size:11px; text-align:center;">LOGO<br>CLIENT</div>'

html_facture = f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<div style="font-family:'Inter', sans-serif; background:#ffffff; color:#111827; border-radius:16px; box-shadow:0 10px 30px rgba(0,0,0,0.08); border:1px solid #e5e7eb; overflow:hidden; max-width:750px; margin:auto;">

  <!-- HEADER -->
  <div style="background:linear-gradient(135deg, #111827 0%, #1f2937 100%); color:white; padding:28px 32px; display:flex; justify-content:space-between; align-items:center;">
    <div style="display:flex; gap:18px; align-items:center;">
      {logo_html}
      <div>
        <h1 style="margin:0; font-size:22px; font-weight:700; letter-spacing:-0.5px;">{st.session_state.boutique_nom}</h1>
        <p style="margin:4px 0 0 0; font-size:13px; opacity:0.8; font-weight:400;">{st.session_state.boutique_adresse}</p>
        <p style="margin:2px 0 0 0; font-size:13px; opacity:0.8;">{st.session_state.boutique_tel} • {st.session_state.boutique_email}</p>
      </div>
    </div>
    <div style="text-align:right;">
      <p style="margin:0; font-size:11px; letter-spacing:2px; opacity:0.6; font-weight:600;">FACTURE</p>
      <p style="margin:6px 0 0 0; font-size:20px; font-weight:700; font-family:'JetBrains Mono', monospace;">{code_facture}</p>
      <p style="margin:4px 0 0 0; font-size:12px; opacity:0.7;">{date_fact.strftime('%d %b %Y')}</p>
    </div>
  </div>

  <!-- INFOS CLIENT / AGENT -->
  <div style="padding:24px 32px; display:flex; justify-content:space-between; background:#f9fafb; border-bottom:1px solid #e5e7eb;">
    <div>
      <p style="margin:0 0 6px 0; font-size:10px; letter-spacing:1.5px; color:#6b7280; font-weight:600;">FACTURÉ À</p>
      <p style="margin:0; font-size:15px; font-weight:600;">{client_nom if client_nom else 'Nom du client'}</p>
      <p style="margin:2px 0 0 0; font-size:13px; color:#4b5563;">{client_tel if client_tel else 'Téléphone client'}</p>
    </div>
    <div style="text-align:right;">
      <p style="margin:0 0 6px 0; font-size:10px; letter-spacing:1.5px; color:#6b7280; font-weight:600;">VENDU PAR</p>
      <p style="margin:0; font-size:14px; font-weight:600; color:#111827;">{agent if agent else 'Agent'}</p>
      <p style="margin:2px 0 0 0; font-size:12px; color:#6b7280; font-family:'JetBrains Mono', monospace;">Exécuté par: {agent if agent else '-'}</p>
    </div>
  </div>

  <!-- TABLE -->
  <div style="padding:0 32px;">
    <table style="width:100%; border-collapse:collapse; margin-top:20px; font-size:13px;">
      <thead>
        <tr style="text-align:left; color:#6b7280; font-size:11px; letter-spacing:0.8px; border-bottom:1px solid #e5e7eb;">
          <th style="padding:12px 0; font-weight:600;">#</th>
          <th style="padding:12px 0; font-weight:600;">DÉSIGNATION & IMEI</th>
          <th style="padding:12px 0; font-weight:600; text-align:center;">QTÉ</th>
          <th style="padding:12px 0; font-weight:600; text-align:right;">PRIX</th>
        </tr>
      </thead>
      <tbody>
"""

for idx, l in enumerate(st.session_state.lignes, 1):
    if not l["designation"]:
        continue
    html_facture += f"""
        <tr style="border-bottom:1px solid #f3f4f6;">
          <td style="padding:14px 0; color:#9ca3af; font-family:'JetBrains Mono', monospace;">{idx:02d}</td>
          <td style="padding:14px 0;">
            <div style="font-weight:600; font-size:13.5px;">{l['designation']}</div>
            <div style="font-size:11px; color:#6b7280; font-family:'JetBrains Mono', monospace; margin-top:2px;">IMEI: {l['imei'] if l['imei'] else '—'}</div>
          </td>
          <td style="padding:14px 0; text-align:center; font-weight:600;">{l['qte']}</td>
          <td style="padding:14px 0; text-align:right; font-weight:600; font-family:'JetBrains Mono', monospace;">{l['prix']*l['qte']:,} F</td>
        </tr>
"""

html_facture += f"""
      </tbody>
    </table>

    <!-- TOTAL -->
    <div style="display:flex; justify-content:flex-end; margin-top:20px;">
      <div style="width:260px; background:#111827; color:white; border-radius:12px; padding:16px 20px; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:11px; letter-spacing:1.5px; opacity:0.7;">TOTAL À PAYER</span>
        <span style="font-size:18px; font-weight:700; font-family:'JetBrains Mono', monospace;">{total:,} F</span>
      </div>
    </div>

    <!-- SIGNATURES -->
    <div style="display:flex; justify-content:space-between; margin-top:48px; padding-top:24px; border-top:1px dashed #d1d5db;">
      <div style="text-align:center; width:45%;">
        <p style="margin:0 0 40px 0; font-size:10px; letter-spacing:1.2px; color:#9ca3af; font-weight:600;">SIGNATURE CLIENT</p>
        <div style="border-top:1px solid #111827; width:80%; margin:0 auto;"></div>
      </div>
      <div style="text-align:center; width:45%;">
        <p style="margin:0 0 8px 0; font-size:10px; letter-spacing:1.2px; color:#9ca3af; font-weight:600;">POUR {st.session_state.boutique_nom}</p>
        <p style="margin:0 0 30px 0; font-size:12px; color:#4b5563;">Agent: {agent}</p>
        <div style="border-top:1px solid #111827; width:80%; margin:0 auto;"></div>
        <p style="margin:6px 0 0 0; font-size:10px; color:#9ca3af;">Cachet & Signature</p>
      </div>
    </div>

    <!-- FOOTER -->
    <div style="text-align:center; margin-top:32px; padding:14px; background:#f9fafb; border-radius:0 0 16px 16px; font-size:10px; color:#9ca3af; letter-spacing:0.5px;">
      Merci pour votre confiance • Téléphone vendu en l'état • {code_facture} • Document généré par ENAM PHONE PRO
    </div>
  </div>
</div>
"""

st.markdown(html_facture, unsafe_allow_html=True)

# --- SAVE ---
if st.button("💾 Enregistrer facture PRO", type="primary", use_container_width=True):
    data = {"code": code_facture, "date": str(date_fact), "client": client_nom, "client_tel": client_tel, "agent": agent, "boutique": st.session_state.boutique_nom, "lignes": st.session_state.lignes, "total": total}
    all_f = []
    if os.path.exists("factures.json"):
        try:
            with open("factures.json","r") as f:
                all_f = json.load(f)
        except:
            all_f = []
    all_f.append(data)
    with open("factures.json","w") as f:
        json.dump(all_f, f, indent=2, ensure_ascii=False)
    st.success(f"Facture {code_facture} enregistrée")
    st.balloons()