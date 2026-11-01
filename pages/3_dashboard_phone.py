import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import hashlib
import io
import os
import json

SHOP_CONFIG = "shop_config.json"
def load_shop_name():
    if os.path.exists(SHOP_CONFIG):
        try:
            with open(SHOP_CONFIG, "r", encoding="utf-8") as f:
                return json.load(f).get("shop_name", "eppro")
        except:
            return "eppro"
    return "eppro"

def save_shop_name(name):
    try:
        with open(SHOP_CONFIG, "w", encoding="utf-8") as f:
            json.dump({"shop_name": name}, f, ensure_ascii=False, indent=2)
    except:
        pass

SHOP_NAME_DEFAULT = load_shop_name()

def check_activation():
    if os.path.exists("licence.json"):
        try:
            with open("licence.json", "r") as f:
                data = json.load(f)
                if not data.get("active", False):
                    return False
                exp_str = data.get("expires_at", "")
                if exp_str:
                    exp = datetime.fromisoformat(exp_str)
                    if datetime.now() > exp:
                        try:
                            os.remove("licence.json")
                            if os.path.exists(SHOP_CONFIG):
                                os.remove(SHOP_CONFIG)
                        except:
                            pass
                        return False
                return True
        except:
            return False
    return False

ACTIVATED = check_activation()

st.set_page_config(page_title="eppro", layout="wide", page_icon="📱")
st.link_button("💳 S'ABONNER - 5000FCFA/MOIS", "Abonnement",use_container_width=True)
st.divider()

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

def fcfa(x):
    return f"{x:,.0f} FCFA".replace(",", " ")

if "df" not in st.session_state:
    data = {
        "IMEI": ["356789101234567", "358923456789012", "351112334455667", "359001122334455"],
        "Modèle": ["Tecno Spark 20", "Infinix Hot 40", "iPhone 14", "Tecno Pop 8"],
        "Marque": ["Tecno", "Infinix", "iPhone", "Tecno"],
        "Prix Achat (FCFA)": [68000,72000,420000,45000],
        "Prix de vente (FCFA)": [85000,92000,525000,58000],
        "👤 Manager / Vendeur": ["ENAM", "Koffi", "ENAM", "Koffi"],
        "📦 Statut": ["En Stock", "En Stock", "En Stock", "En Stock"]
    }
    st.session_state.df = pd.DataFrame(data)
    st.session_state.df["💰 Profit"] = st.session_state.df["Prix de vente (FCFA)"] - st.session_state.df["Prix Achat (FCFA)"]

if "historique_ventes" not in st.session_state:
    st.session_state.historique_ventes = []
if "licence_active" not in st.session_state:
    st.session_state.licence_active = False

with st.sidebar:
    st.header("⚙️ Config Boutique")
    boutique = st.text_input("🏪 Nom de votre boutique", value=SHOP_NAME_DEFAULT)
    if boutique and boutique != SHOP_NAME_DEFAULT:
        save_shop_name(boutique)
    st.file_uploader("🖼️ Logo de la boutique (PNG/JPG)", type=["png","jpg","jpeg"])
    st.divider()
    st.markdown("### 🔍 Filtrer le Stock")
    marques = ["Toutes"] + list(st.session_state.df["Marque"].unique())
    filtre_marque = st.selectbox("🏷️ Filtrer par marque", marques)
    filtre_statut = st.selectbox("📦 Filtrer par statut", ["Tous", "En Stock", "Vendu"])
    st.divider()
    st.markdown("### ➕ Ajouter un Téléphone")
    with st.form("ajout_phone", clear_on_submit=True):
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
                st.error("❌ Remplis IMEI, Modèle et Manager")
    st.divider()
    st.markdown("### 🔒 Licence PRO")
    if not st.session_state.licence_active and not ACTIVATED:
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
        st.success(f"✅ Active: {st.session_state.get('licence_key','')}")
        if st.button("🔓 Déconnecter"):
            st.session_state.licence_active = False
            st.rerun()
    st.divider()
    st.caption(f"👨‍💻 Dev par ENAM\n📲 Flooz: {FLOOZ}\n📲 TMoney: {TMONEY}")

df_affiche = st.session_state.df.copy()
if filtre_marque != "Toutes":
    df_affiche = df_affiche[df_affiche["Marque"] == filtre_marque]
if filtre_statut != "Tous":
    df_affiche = df_affiche[df_affiche["📦 Statut"] == filtre_statut]

st.markdown(f'<div class="header"><h1>📱 {boutique}</h1><p>Dashboard qui fait gagner du temps et de l argent - Propulsé par Enam</p></div>', unsafe_allow_html=True)
st.write("")

c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">📦 Appareils Filtrés</div><div class="kpi-value">{len(df_affiche)}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">💼 Valeur Stock</div><div class="kpi-value">{fcfa(df_affiche[df_affiche["📦 Statut"]=="En Stock"]["Prix Achat (FCFA)"].sum())}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">📈 Profit Total</div><div class="kpi-value">{fcfa(df_affiche["💰 Profit"].sum())}</div></div>', unsafe_allow_html=True)
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
    
    # === BLOC VENDRE MODIFIE - 7 CHAMPS OBLIGATOIRES ===
    st.subheader("💸 Vendre un téléphone")
    stock_dispo = df_affiche[df_affiche["📦 Statut"]=="En Stock"]
    if len(stock_dispo)>0:
        phone_a_vendre = st.selectbox("📱 Choisir IMEI à vendre", stock_dispo["IMEI"].tolist())
        
        if phone_a_vendre:
            row_sel = st.session_state.df[st.session_state.df["IMEI"]==phone_a_vendre].iloc[0]
            modele_auto = row_sel["Modèle"]
            marque_auto = row_sel["Marque"]
            prix_auto = row_sel["Prix de vente (FCFA)"]
        else:
            modele_auto = ""
            marque_auto = ""
            prix_auto = 0

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.text_input("📲 Modèle", value=modele_auto, disabled=True, key="v_modele")
            st.text_input("🏷️ Marque", value=marque_auto, disabled=True, key="v_marque")
            st.text_input("💰 Prix de vente", value=fcfa(prix_auto) if prix_auto else "", disabled=True, key="v_prix")
        with col_v2:
            client = st.text_input("👤 Client", placeholder="Nom du client", key="v_client")
            vendeur = st.text_input("👤 Qui vend? (Manager)", placeholder="Ex: ENAM", key="v_vendeur")
            code_manager = st.text_input("🔑 Code Manager", placeholder="Code secret manager", type="password", key="v_code")

        champs_remplis = all([
            phone_a_vendre, 
            modele_auto!="", 
            marque_auto!="", 
            prix_auto>0, 
            client.strip()!="", 
            vendeur.strip()!="", 
            code_manager.strip()!=""
        ])
        
        if not champs_remplis:
            st.warning("⚠️ Remplis IMEI + Modèle + Marque + Prix + Client + Manager + Code Manager")

        if st.button("🔥 Confirmer Vente", disabled=not champs_remplis, use_container_width=True):
            idx = st.session_state.df[st.session_state.df["IMEI"]==phone_a_vendre].index[0]
            st.session_state.df.at[idx, "📦 Statut"] = "Vendu"
            if vendeur:
                st.session_state.df.at[idx, "👤 Manager / Vendeur"] = vendeur
            st.session_state.historique_ventes.append({
                "IMEI": phone_a_vendre,
                "Modèle": modele_auto,
                "Marque": marque_auto,
                "Prix": prix_auto,
                "Client": client,
                "👤 Vendeur": vendeur,
                "🔑 Code": code_manager,
                "📅 Date": datetime.now().strftime("%d/%m %H:%M")
            })
            st.success(f"🎉 Vendu à {client} par {vendeur}! {fcfa(prix_auto)}")
            st.balloons()
            st.rerun()
    else:
        st.info("📦 Aucun téléphone en stock")

    st.subheader("📜 Historique des ventes")
    if st.session_state.historique_ventes:
        st.table(pd.DataFrame(st.session_state.historique_ventes))
    else:
        st.info("Aucune vente encore")
    st.divider()
    st.subheader("📤 Exporter & Télécharger")
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        if st.session_state.licence_active or ACTIVATED:
            csv = st.session_state.df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 TÉLÉCHARGER CSV PRO", csv, "rapport_enam_manager.csv", "text/csv", type="primary", use_container_width=True)
        else:
            st.warning("🔒 Active ta licence pour CSV")
    with col_exp2:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.df.to_excel(writer, index=False, sheet_name='Stock Complet')
            df_affiche.to_excel(writer, index=False, sheet_name='Stock Filtre')
            if st.session_state.historique_ventes:
                pd.DataFrame(st.session_state.historique_ventes).to_excel(writer, index=False, sheet_name='Historique Ventes')
        st.download_button(
            label="📊 TÉLÉCHARGER FEUILLE EXCEL (Stock + Filtre + Ventes)",
            data=output.getvalue(), file_name=f"eppro_{datetime.now().strftime('%d-%m-%Y')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        st.caption("✅ Excel contient 3 onglets: Stock Complet, Stock Filtré, Historique Ventes avec Manager")

# === RESET PAR CLE ADMIN ===
st.divider()
if ACTIVATED:
    try:
        with open("licence.json","r") as f:
            lic_data = json.load(f)
            type_abo = lic_data.get("type", "mensuel")
            cle_stockee = lic_data.get("key", "")
            exp = datetime.fromisoformat(lic_data.get("expires_at",""))
            jours = (exp - datetime.now()).days
            st.success(f"✅ Licence {type_abo} active - Expire {exp.strftime('%d/%m/%Y')} ({jours}j) - eppro conservé")
    except:
        type_abo = "mensuel"
        cle_stockee = ""
        st.success("✅ Licence active - Espace client eppro")

    col_reset1, col_reset2 = st.columns(2)
    with col_reset1:
        st.markdown(f"#### ⚠️ RESET TOTAL - {type_abo.upper()}")
        st.caption(f"Clé admin {type_abo} requise")
        cle_reset = st.text_input(f"🔑 Entre ta clé {type_abo} pour RESET", type="password", key="cle_reset_admin")
        if st.button("⚠️ RESET TOTAL - Tout effacer (CLIENT VIDE)", type="secondary", use_container_width=True):
            if cle_reset and cle_stockee and cle_reset == cle_stockee:
                st.session_state.df = pd.DataFrame(columns=["IMEI","Modèle","Marque","Prix Achat (FCFA)","Prix de vente (FCFA)","👤 Manager / Vendeur","📦 Statut","💰 Profit"])
                st.session_state.historique_ventes = []
                st.success(f"📦 Stock à zéro - Reset {type_abo} validé")
                st.rerun()
            elif not cle_reset:
                st.error("❌ Entre ta clé admin")
            else:
                st.error(f"❌ Clé invalide - Clé {type_abo} requise")
    with col_reset2:
        st.markdown("#### 🎬 MODE DÉMO")
        if st.button("🎬 REMETTRE MODE DÉMO - 4 téléphones", type="primary", use_container_width=True):
            data_demo = {
                "IMEI": ["356789101234567", "358923456789012", "351112334455667", "359001122334455"],
                "Modèle": ["Tecno Spark 20", "Infinix Hot 40", "iPhone 14", "Tecno Pop 8"],
                "Marque": ["Tecno", "Infinix", "iPhone", "Tecno"],
                "Prix Achat (FCFA)": [68000,72000,420000,45000],
                "Prix de vente (FCFA)": [85000,92000,525000,58000],
                "👤 Manager / Vendeur": ["ENAM", "Koffi", "ENAM", "Koffi"],
                "📦 Statut": ["En Stock", "En Stock", "En Stock", "En Stock"]
            }
            st.session_state.df = pd.DataFrame(data_demo)
            st.session_state.df["💰 Profit"] = st.session_state.df["Prix de vente (FCFA)"] - st.session_state.df["Prix Achat (FCFA)"]
            st.success("🎬 Mode démo remis")
            st.rerun()
else:
    st.warning("🔒 RESET bloqué - Active avec clé admin mensuel/annuel")
    col1_b, col2_b = st.columns(2)
    with col1_b:
        st.button("⚠️ RESET TOTAL - Clé admin requise", disabled=True, use_container_width=True)
    with col2_b:
        if st.button("🎬 MODE DÉMO - Voir démonstration", type="primary", use_container_width=True):
            data_demo = {
                "IMEI": ["356789101234567", "358923456789012", "351112334455667", "359001122334455"],
                "Modèle": ["Tecno Spark 20", "Infinix Hot 40", "iPhone 14", "Tecno Pop 8"],
                "Marque": ["Tecno", "Infinix", "iPhone", "Tecno"],
                "Prix Achat (FCFA)": [68000,72000,420000,45000],
                "Prix de vente (FCFA)": [85000,92000,525000,58000],
                "👤 Manager / Vendeur": ["ENAM", "Koffi", "ENAM", "Koffi"],
                "📦 Statut": ["En Stock", "En Stock", "En Stock", "En Stock"]
            }
            st.session_state.df = pd.DataFrame(data_demo)
            st.session_state.df["💰 Profit"] = st.session_state.df["Prix de vente (FCFA)"] - st.session_state.df["Prix Achat (FCFA)"]
            st.rerun()
