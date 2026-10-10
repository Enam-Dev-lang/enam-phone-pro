import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="ENAM PHONE PRO", page_icon="📱", layout="wide")

# --- STYLE LUXE ---
st.markdown("""
<style>
   .header { background: linear-gradient(90deg, #0A1931 0%, #185ADB 100%); padding: 20px; border-radius: 15px; color: white; display:flex; align-items:center; gap:20px; }
   .kpi-card { background: white; padding: 18px; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); border-top: 5px solid #185ADB; text-align: center; }
   .kpi-value { font-size: 24px; font-weight: 900; color: #0A1931; }
   .kpi-label { font-size: 12px; color: #6c757d; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

def fcfa(x): return f"{x:,.0f} FCFA".replace(",", " ")

# --- DONNEES EN MEMOIRE ---
if "df" not in st.session_state:
    data = {
        "IMEI": ["356789101234567", "358923456789012", "351112334455667", "359001122334455", "357778899001122"],
        "Modèle": ["Tecno Spark 20", "Infinix Hot 40", "iPhone 14", "Tecno Pop 8", "Infinix Smart 8"],
        "Marque": ["Tecno", "Infinix", "iPhone", "Tecno", "Infinix"],
        "Prix Achat (FCFA)": [68000, 72000, 420000, 45000, 110000],
        "Prix de vente (FCFA)": [85000, 92000, 525000, 58000, 135000],
        "Statut": ["En stock", "En stock", "En stock", "En stock", "Vendu"],
        "Client": ["-", "-", "Koffi", "-", "Afi"],
    }
    st.session_state.df = pd.DataFrame(data)
    st.session_state.df["Profit(FCFA)"] = st.session_state.df["Prix de vente (FCFA)"] - st.session_state.df["Prix Achat (FCFA)"]

df = st.session_state.df

# --- SIDEBAR CLIENT - FONCTION 1 ---
with st.sidebar:
    st.title("⚙️ Config Boutique")
    nom_boutique = st.text_input("Nom de votre boutique", "ENAM PHONE - Lomé")
    logo = st.file_uploader("Logo de la boutique (PNG/JPG)", type=["png","jpg","jpeg"])
    st.divider()
    st.write("👨‍💻 Dev par ENAM")
    st.caption("Vente : 50 000 FCFA / licence")

# --- HEADER AVEC LOGO ---
col_logo, col_titre = st.columns([1,5])
with col_logo:
    if logo: st.image(logo, width=120)
with col_titre:
    st.markdown(f'<div class="header"><div><h1 style="margin:0;color:white;">📱 {nom_boutique}</h1><p style="margin:0;">Dashboard qui fait gagner de l\'argent - Propulsé par ENAM</p></div></div>', unsafe_allow_html=True)

st.write("")

# --- FILTRE ---
marques = ["Toutes"] + sorted(df["Marque"].unique().tolist())
choix = st.selectbox("🔍 Filtrer par marque", marques)
df_f = df if choix == "Toutes" else df[df["Marque"] == choix]

# --- KPI ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">📦 Appareils</div><div class="kpi-value">{len(df_f)}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">💰 Valeur Stock</div><div class="kpi-value">{fcfa(df_f["Prix Achat (FCFA)"].sum())}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">📈 Profit</div><div class="kpi-value">{fcfa(df_f["Profit(FCFA)"].sum())}</div></div>', unsafe_allow_html=True)
with c4:
    try: star = df_f.groupby("Marque")["Profit(FCFA)"].sum().idxmax()
    except: star = "-"
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">🔥 Marque Star</div><div class="kpi-value">{star}</div></div>', unsafe_allow_html=True)

st.write("")

# --- FONCTION 2 - AJOUTER TELEPHONE ---
with st.expander("➕ AJOUTER UN NOUVEAU TÉLÉPHONE (sans toucher au code)", expanded=False):
    with st.form("add_form", clear_on_submit=True):
        c_a, c_b, c_c = st.columns(3)
        imei = c_a.text_input("IMEI")
        modele = c_b.text_input("Modèle", "Tecno Spark 30")
        marque = c_c.selectbox("Marque", ["Tecno","Infinix","iPhone","Samsung","Itel"])
        c_d, c_e, c_f = st.columns(3)
        achat = c_d.number_input("Prix Achat", min_value=0, value=70000, step=1000)
        vente = c_e.number_input("Prix Vente", min_value=0, value=90000, step=1000)
        statut = c_f.selectbox("Statut", ["En stock","Vendu"])
        client = st.text_input("Client (si vendu)", "-")
        submit = st.form_submit_button("✅ Ajouter au stock", width='stretch')
        if submit:
            nouveau = {"IMEI": imei, "Modèle": modele, "Marque": marque, "Prix Achat (FCFA)": achat, "Prix de vente (FCFA)": vente, "Statut": statut, "Client": client, "Profit(FCFA)": vente-achat}
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nouveau])], ignore_index=True)
            st.success(f"{modele} ajouté!")
            st.rerun()

# --- GRAPHIQUE + TABLEAU ---
gauche, droite = st.columns([1.2, 2])
with gauche:
    st.subheader("💎 Profit par marque")
    fig = px.bar(df_f.groupby("Marque")["Profit(FCFA)"].sum().reset_index(), x="Marque", y="Profit(FCFA)", color="Marque", color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(showlegend=False, height=350, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, width='stretch')
with droite:
    st.subheader("📋 Stock en temps réel")
    st.dataframe(df_f, width='stretch', hide_index=True, height=350)

st.divider()

col_a, col_b = st.columns([2,1])
with col_a:
    st.subheader("💰 Simulateur rapide")
    ca, cv = st.columns(2)
    a = ca.number_input("Prix Achat Test", value=68000, key="sim_achat")
    v = cv.number_input("Prix Vente Test", value=85000, key="sim_vente")
    b = v - a
    if b > 0: st.success(f"Bénéfice: {fcfa(b)}")
    else: st.error(f"Perte: {fcfa(b)}")

with col_b:
    st.subheader("📤 Rapport Pro")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_f.to_excel(writer, index=False, sheet_name="Stock")
    st.download_button("📥 TÉLÉCHARGER LE RAPPORT", buffer.getvalue(), f"Rapport_{nom_boutique}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", width='stretch', type="primary")