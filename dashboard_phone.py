import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import hashlib
import io

st.set_page_config(page_title="MANAGEMENT PHONE SHOP BY ENAM", layout="wide", page_icon="📱")

FLOOZ = "+228 97 04 42 09"
TMONEY = "+228 91 29 63 08"
PRIX_MOIS = 5000
PRIX_AN = 50000

# --- STYLE LUXE ---
st.markdown("""
<style>
.header { background: linear-gradient(90deg, #0A1931 0%, #185ADB 100%); padding:20px; border-radius:15px; color:white; text-align:center; }
.kpi-card { background: white; padding: 18px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align:center; }
.kpi-value { font-size: 24px; font-weight: 900; color: #0A1931; }
.kpi-label { font-size: 12px; color: #6c757d; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

def fcfa(x): return f"{x:,.0f} FCFA".replace(",", " ")

if "df" not in st.session_state:
    data = {
        "IMEI": ["356789101234567", "358923456789012", "351112334455667", "359001122334455", "357778899001122"],
        "Modèle": ["Tecno Spark 20", "Infinix Hot 40", "iPhone 14", "Tecno Pop 8", "Infinix Smart 8"],
        "Marque": ["Tecno", "Infinix", "iPhone", "Tecno", "Infinix"],
        "Prix Achat (FCFA)": [68000,72000,420000,45000,110000],
        "Prix de vente (FCFA)": [85000,92000,525000,58000,135000]
    }
    st.session_state.df = pd.DataFrame(data)
    st.session_state.df["Profit"] = st.session_state.df["Prix de vente (FCFA)"] - st.session_state.df["Prix Achat (FCFA)"]

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Config Boutique")
    boutique = st.text_input("Nom de votre boutique", "MANAGEMENT PHONE SHOP - Lomé")
    st.file_uploader("Logo de la boutique (PNG/JPG)", type=["png","jpg","jpeg"])
    st.divider()
    st.markdown("### 🔒 Licence PRO")
    if "licence_active" not in st.session_state:
        st.session_state.licence_active = False
    if not st.session_state.licence_active:
        plan = st.radio("Choisissez abonnement:", [f"Mois - {PRIX_MOIS} FCFA", f"An - {PRIX_AN} FCFA (Meilleur)"])
        st.info(f"Payez sur:\n\n**Flooz: {FLOOZ}**\n\n**TMoney: {TMONEY}**")
        num_payeur = st.text_input("Votre numéro qui a payé")
        id_trans = st.text_input("ID Transaction")
        if st.button("✅ J'ai payé, Activer"):
            if num_payeur and id_trans:
                key = "ENAM-" + hashlib.md5(f"{boutique}{id_trans}{datetime.now()}".encode()).hexdigest()[:8].upper()
                st.session_state.licence_active = True
                st.session_state.licence_key = key
                st.success(f"Licence activée: {key}")
                st.balloons()
            else:
                st.error("Rentre numéro et ID transaction")
    else:
        st.success(f"✅ Active: {st.session_state.licence_key}")
        if st.button("Déconnecter"):
            st.session_state.licence_active = False
            st.rerun()
    st.divider()
    st.caption(f"👨‍💻 Dev par ENAM\nFlooz: {FLOOZ}\nTMoney: {TMONEY}")

# --- HEADER ---
st.markdown(f'<div class="header"><h1>📱 {boutique}</h1><p>Dashboard qui fait gagner de l argent - Propulsé par ENAM</p></div>', unsafe_allow_html=True)
st.write("")

df = st.session_state.df
# METRICS
c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Appareils</div><div class="kpi-value">{len(df)}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Valeur Stock</div><div class="kpi-value">{fcfa(df["Prix Achat (FCFA)"].sum())}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Profit</div><div class="kpi-value">{fcfa(df["Profit"].sum())}</div></div>', unsafe_allow_html=True)
with c4: 
    star = df.groupby("Marque")["Profit"].sum().idxmax() if len(df)>0 else "-"
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Marque Star</div><div class="kpi-value">{star}</div></div>', unsafe_allow_html=True)

st.write("")
col1, col2 = st.columns([1,2])
with col1:
    st.subheader("💎 Profit par marque")
    fig = px.bar(df.groupby("Marque")["Profit"].sum().reset_index(), x="Marque", y="Profit", color="Marque", color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("💰 Simulateur rapide")
    achat = st.number_input("Prix Achat Test", value=68000, step=1000)
    vente = st.number_input("Prix Vente Test", value=85000, step=1000)
    st.success(f"Bénéfice: {fcfa(vente-achat)}")
with col2:
    st.subheader("📋 Stock en temps réel")
    st.dataframe(df, use_container_width=True)
    if st.session_state.licence_active:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 TÉLÉCHARGER LE RAPPORT PRO", csv, "rapport_enam.csv", "text/csv", type="primary", use_container_width=True)
    else:
        st.warning("🔒 Active ta licence pour télécharger")