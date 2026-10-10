import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import hashlib

# CONFIG
st.set_page_config(page_title="MANAGEMENT PHONE SHOP PRO by @Enam", layout="wide", page_icon="📱")
FLOOZ = "+228 97 04 42 09"
TMONEY = "+228 91 29 63 08"
PRIX_MOIS = 5000
PRIX_AN = 50000

# --- CSS ---
st.markdown("""
<style>
.main-header {background: linear-gradient(90deg, #0a1931 0%, #185ADB 100%); padding:20px; border-radius:15px; color:white; text-align:center;}
.prix-box {border:2px solid #185ADB; border-radius:12px; padding:15px; text-align:center; background:#f0f4ff;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONFIG + PAIEMENT ---
with st.sidebar:
    st.header("⚙️ Config Boutique")
    boutique = st.text_input("Nom de votre boutique", "MANAGEMENT PHONE SHOP - Lomé")
    logo = st.file_uploader("Logo de la boutique (PNG/JPG)", type=["png","jpg","jpeg"])
    if logo:
        st.image(logo, width=150)
    
    st.divider()
    st.markdown("### 🔒 Licence PRO")
    st.caption("Vente : 5 000F / mois ou 50 000F / an")
    
    # Vérif licence simple (stockée dans session)
    if "licence_active" not in st.session_state:
        st.session_state.licence_active = False
    
    if not st.session_state.licence_active:
        plan = st.radio("Choisissez votre abonnement:", [f"Mois - {PRIX_MOIS} FCFA", f"An - {PRIX_AN} FCFA (Meilleur)"])
        st.info(f"Payez sur:\n\n**Flooz: {FLOOZ}**\n\n**TMoney: {TMONEY}**")
        num_payeur = st.text_input("Votre numéro qui a payé")
        id_trans = st.text_input("ID Transaction Flooz/TMoney")
        if st.button("✅ J'ai payé, Activer ma licence"):
            if num_payeur and id_trans:
                # Génère clé licence
                key_base = f"{boutique}{id_trans}{datetime.now()}"
                licence_key = "ENAM-" + hashlib.md5(key_base.encode()).hexdigest()[:8].upper()
                st.session_state.licence_active = True
                st.session_state.licence_key = licence_key
                st.success(f"Licence activée ! Clé: {licence_key}")
                st.balloons()
            else:
                st.error("Rentre ton numéro et l'ID transaction")
    else:
        st.success(f"✅ Licence Active: {st.session_state.licence_key}")
        if st.button("Se déconnecter"):
            st.session_state.licence_active = False
            st.rerun()

    st.divider()
    st.markdown("👨‍💻 Dev par ENAM")
    st.caption(f"Flooz: {FLOOZ}\nTMoney: {TMONEY}")

# --- HEADER ---
st.markdown(f'<div class="main-header"><h1>📱 {boutique}</h1><p>Dashboard qui fait gagner de l\'argent - Propulsé par ENAM</p></div>', unsafe_allow_html=True)

# --- DONNÉES DE DÉMO (remplace par ton Excel) ---
data = {
    "IMEI": ["356789101234567","358923456789012","351112334455667","359001122334455","357778899001122"],
    "Modèle": ["Tecno Spark 20","Infinix Hot 40","iPhone 14","Tecno Pop 8","Infinix Smart 8"],
    "Marque": ["Tecno","Infinix","iPhone","Tecno","Infinix"],
    "Prix Achat (FCFA)": [68000,72000,420000,45000,110000],
    "Prix de vente (FCFA)": [85000,92000,525000,58000,135000]
}
df = pd.DataFrame(data)
df["Profit"] = df["Prix de vente (FCFA)"] - df["Prix Achat (FCFA)"]

# --- METRIQUES ---
c1,c2,c3,c4 = st.columns(4)
c1.metric("📦 APPAREILS", len(df))
c2.metric("💰 VALEUR STOCK", f"{df['Prix Achat (FCFA)'].sum():,} FCFA")
c3.metric("📈 PROFIT", f"{df['Profit'].sum():,} FCFA")
c4.metric("🔥 MARQUE STAR", df.groupby("Marque")["Profit"].sum().idxmax())

# --- GRAPHIQUE ---
col_g1, col_g2 = st.columns([1,2])
with col_g1:
    st.subheader("💎 Profit par marque")
    fig = px.bar(df.groupby("Marque")["Profit"].sum().reset_index(), x="Marque", y="Profit", color="Marque", color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("💰 Simulateur rapide")
    achat = st.number_input("Prix Achat Test", value=68000, step=1000)
    vente = st.number_input("Prix Vente Test", value=85000, step=1000)
    st.success(f"Bénéfice: {vente-achat:,} FCFA")

with col_g2:
    st.subheader("📋 Stock en temps réel")
    st.dataframe(df, use_container_width=True)
    if st.session_state.licence_active:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 TÉLÉCHARGER LE RAPPORT PRO (Excel)", csv, "rapport_enam.csv", "text/csv")
    else:
        st.warning("🔒 Active ta licence pour télécharger le rapport complet")
        st.button("📥 TÉLÉCHARGER LE RAPPORT - Version bloquée")