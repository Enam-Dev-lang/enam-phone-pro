import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import hashlib

st.set_page_config(page_title="MANAGEMENT PHONE SHOP BY ENAM", layout="wide", page_icon="📱")

FLOOZ = "+228 97 04 42 09"
TMONEY = "+228 91 29 63 08"
PRIX_MOIS = 5000
PRIX_AN = 50000

st.markdown("""
<style>
.header { background: linear-gradient(90deg, #0A1931 0%, #185ADB 100%); padding:20px; border-radius:15px; color:white; text-align:center; }
.kpi-card { background: white; padding: 18px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align:center; }
.kpi-value { font-size: 22px; font-weight: 900; color: #0A1931; }
.kpi-label { font-size: 11px; color: #6c757d; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

def fcfa(x): return f"{x:,.0f} FCFA".replace(",", " ")

# --- INIT DATA AVEC MANAGER ---
if "df" not in st.session_state:
    data = {
        "IMEI": ["356789101234567", "358923456789012", "351112334455667"],
        "Modèle": ["Tecno Spark 20", "Infinix Hot 40", "iPhone 14"],
        "Marque": ["Tecno", "Infinix", "iPhone"],
        "Prix Achat (FCFA)": [68000,72000,420000],
        "Prix de vente (FCFA)": [85000,92000,525000],
        "👤 Manager / Vendeur": ["ENAM", "Koffi", "ENAM"],
        "📦 Statut": ["En Stock", "En Stock", "Vendu"]
    }
    st.session_state.df = pd.DataFrame(data)
    st.session_state.df["💰 Profit"] = st.session_state.df["Prix de vente (FCFA)"] - st.session_state.df["Prix Achat (FCFA)"]

if "historique_ventes" not in st.session_state:
    st.session_state.historique_ventes = []

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Config Boutique")
    boutique = st.text_input("🏪 Nom de votre boutique", "MANAGEMENT PHONE SHOP - Lomé")
    st.file_uploader("🖼️ Logo de la boutique", type=["png","jpg","jpeg"])

    st.divider()
    st.markdown("### 🔍 Filtrer le Stock")
    marques = ["Toutes"] + list(st.session_state.df["Marque"].unique())
    filtre_marque = st.selectbox("🏷️ Filtrer par marque", marques)
    filtre_statut = st.selectbox("📦 Filtrer par statut", ["Tous", "En Stock", "Vendu"])

    st.divider()
    st.markdown("### ➕ Ajouter un Téléphone")
    with st.form("ajout_phone"):
        imei = st.text_input("📱 IMEI")
        modele = st.text_input("📲 Modèle (ex: Spark 20)")
        marque = st.selectbox("🏷️ Marque", ["Tecno","Infinix","iPhone","Samsung","Itel","Autre"])
        prix_achat = st.number_input("💸 Prix Achat", min_value=0, step=1000)
        prix_vente = st.number_input("💰 Prix Vente", min_value=0, step=1000)
        manager_ajout = st.text_input("👤 Manager qui restocke", placeholder="Ex: ENAM, Koffi...")
        submitted = st.form_submit_button("✅ Ajouter au Stock")
        if submitted:
            if imei and modele and manager_ajout:
                new_row = {"IMEI": imei, "Modèle": modele, "Marque": marque, "Prix Achat (FCFA)": prix_achat, "Prix de vente (FCFA)": prix_vente, "👤 Manager / Vendeur": manager_ajout, "📦 Statut": "En Stock", "💰 Profit": prix_vente-prix_achat}
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"📱 {modele} ajouté par {manager_ajout}!")
            else:
                st.error("Remplis IMEI, Modèle et Manager")

    st.divider()
    st.markdown("### 🔒 Licence PRO")
    if "licence_active" not in st.session_state:
        st.session_state.licence_active = False
    if not st.session_state.licence_active:
        plan = st.radio("💳 Choisissez abonnement:", [f"📅 Mois - {PRIX_MOIS} FCFA", f"🏆 An - {PRIX_AN} FCFA (Meilleur)"])
        st.info(f"💸 Payez sur:\n\n**📲 Flooz: {FLOOZ}**\n\n**📲 TMoney: {TMONEY}**")
        num_payeur = st.text_input("📞 Votre numéro qui a payé")
        id_trans = st.text_input("🧾 ID Transaction")
        if st.button("✅ J'ai payé, Activer"):
            if num_payeur and id_trans:
                key = "ENAM-" + hashlib.md5(f"{boutique}{id_trans}{datetime.now()}".encode()).hexdigest()[:8].upper()
                st.session_state.licence_active = True
                st.session_state.licence_key = key
                st.success(f"✅ Activée: {key}")
                st.balloons()
            else:
                st.error("❌ Rentre numéro et ID")
    else:
        st.success(f"✅ Active: {st.session_state.licence_key}")
        if st.button("🔓 Déconnecter"):
            st.session_state.licence_active = False
            st.rerun()
    st.divider()
    st.caption(f"👨‍💻 Dev par ENAM\n📲 Flooz: {FLOOZ}\n📲 TMoney: {TMONEY}")

# --- FILTRAGE LOGIQUE ---
df_affiche = st.session_state.df.copy()
if filtre_marque!= "Toutes":
    df_affiche = df_affiche[df_affiche["Marque"] == filtre_marque]
if filtre_statut!= "Tous":
    df_affiche = df_affiche[df_affiche["📦 Statut"] == filtre_statut]

# --- HEADER ---
st.markdown(f'<div class="header"><h1>📱 {boutique}</h1><p>💼 Dashboard qui fait gagner du temps et de l argent - Propulsé par ENAM</p></div>', unsafe_allow_html=True)
st.write("")

# --- KPIS AVEC EMOJIS ---
c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">📦 Appareils Filtrés</div><div class="kpi-value">{len(df_affiche)}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">💼 Valeur Stock</div><div class="kpi-value">{fcfa(df_affiche[df_affiche["📦 Statut"]=="En Stock"]["Prix Achat (FCFA)"].sum())}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">📈 Profit Total</div><div class="kpi-value">{fcfa(df_affiche["💰 Profit"].sum())}</div></div>', unsafe_allow_html=True)
with c4:
    star = df_affiche.groupby("Marque")["💰 Profit"].sum().idxmax() if len(df_affiche)>0 else "-"
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">🔥 Marque Star</div><div class="kpi-value">{star}</div></div>', unsafe_allow_html=True)

st.write("")
col1, col2 = st.columns([1,2])

with col1:
    st.subheader("💎 Profit par marque")
    if len(df_affiche)>0:
        fig = px.bar(df_affiche.groupby("Marque")["💰 Profit"].sum().reset_index(), x="Marque", y="💰 Profit", color="Marque")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("👥 Performance par Manager")
    if len(df_affiche)>0:
        fig2 = px.pie(df_affiche.groupby("👤 Manager / Vendeur")["💰 Profit"].sum().reset_index(), values="💰 Profit", names="👤 Manager / Vendeur", hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("💰 Simulateur rapide")
    achat = st.number_input("💸 Prix Achat Test", value=68000, step=1000)
    vente = st.number_input("💵 Prix Vente Test", value=85000, step=1000)
    st.success(f"✅ Bénéfice: {fcfa(vente-achat)}")

with col2:
    st.subheader("📋 Stock en temps réel (avec Manager)")
    st.dataframe(df_affiche, use_container_width=True)

    st.subheader("💸 Vendre un téléphone")
    if len(df_affiche[df_affiche["📦 Statut"]=="En Stock"])>0:
        phone_a_vendre = st.selectbox("📱 Choisir IMEI à vendre", df_affiche[df_affiche["📦 Statut"]=="En Stock"]["IMEI"].tolist())
        vendeur = st.text_input("👤 Qui vend? (Manager)", placeholder="Ex: ENAM")
        if st.button("🔥 Confirmer Vente"):
            idx = st.session_state.df[st.session_state.df["IMEI"]==phone_a_vendre].index[0]
            st.session_state.df.at[idx, "📦 Statut"] = "Vendu"
            st.session_state.df.at[idx, "👤 Manager / Vendeur"] = vendeur if vendeur else st.session_state.df.at[idx, "👤 Manager / Vendeur"]
            st.session_state.historique_ventes.append({"IMEI": phone_a_vendre, "Vendeur": vendeur, "Date": datetime.now().strftime("%d/%m %H:%M")})
            st.success(f"🎉 Vendu par {vendeur}!")
            st.rerun()

    st.subheader("📜 Historique des ventes")
    if st.session_state.historique_ventes:
        st.table(pd.DataFrame(st.session_state.historique_ventes))
    else:
        st.info("Aucune vente encore")

    st.divider()
    st.subheader("📤 Exporter & Télécharger")
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        # CSV pour licence active
        if st.session_state.licence_active:
            csv = st.session_state.df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 TÉLÉCHARGER CSV PRO", csv, "rapport_enam_manager.csv", "text/csv", type="primary", use_container_width=True)
        else:
            st.warning("🔒 Active ta licence pour CSV - Flooz/TMoney")
    
    with col_exp2:
        # EXCEL - TOUJOURS DISPO MEME SANS LICENCE (ou avec licence si tu veux bloquer, change)
        import io
        output = io.BytesIO()
        # On crée un Excel avec 2 feuilles
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.df.to_excel(writer, index=False, sheet_name='📦 Stock Complet')
            df_affiche.to_excel(writer, index=False, sheet_name='🔍 Stock Filtré')
            if st.session_state.historique_ventes:
                pd.DataFrame(st.session_state.historique_ventes).to_excel(writer, index=False, sheet_name='📜 Historique Ventes')
        
        st.download_button(
            label="📊 TÉLÉCHARGER FEUILLE EXCEL (Stock + Filtre + Ventes)",
            data=output.getvalue(),
            file_name=f"MANAGEMENT_PHONE_SHOP_BY_ENAM_{datetime.now().strftime('%d-%m-%Y')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="secondary",
            use_container_width=True
        )
        st.caption("✅ Excel contient 3 onglets: Stock Complet, Stock Filtré, Historique Ventes avec Manager")