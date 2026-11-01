import streamlit as st
import pandas as pd
import os
import json
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Rapport Vendeurs", layout="wide")
st.title("📊 Rapport - Ventes par Vendeur")
FICHIER_STOCK = "stock.xlsx"
CONFIG_FILE = "shop_config.json"
CAISSE_FILE = "caisse_journal.json"

# --- CHARGEMENT CONFIG VENDEURS ---
def load_vendeurs():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            # Tes codes MGR- sont dedans
            return cfg.get("managers", {}), cfg.get("manager_codes", {})
        except:
            return {}, {}
    return {}, {}

managers_map, codes_map = load_vendeurs()

# --- LECTURE DIRECTE DE TON FICHIER ---
if not os.path.exists(FICHIER_STOCK):
    st.warning("stock.xlsx n'existe pas encore. Ajoute un téléphone dans le dashboard phone puis reviens.")
    st.stop()
try:
    df = pd.read_excel(FICHIER_STOCK, dtype={"IMEI": str})
except Exception as e:
    st.error(f"Impossible de lire stock.xlsx : {e}")
    st.stop()
if df.empty:
    st.info("stock.xlsx est vide. Ajoute des téléphones dans le dashboard.")
    st.stop()

# Gère la colonne date
if "date" not in df.columns:
    df["date"] = datetime.now()
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

# Gère colonne vendeur
if "👤 Manager / Vendeur" not in df.columns:
    df["👤 Manager / Vendeur"] = "Patron"
if "💰 Profit" not in df.columns and "Prix Achat (FCFA)" in df.columns and "Prix de vente (FCFA)" in df.columns:
    df["💰 Profit"] = df["Prix de vente (FCFA)"] - df["Prix Achat (FCFA)"]

# --- FILTRES ---
col_f1, col_f2 = st.columns(2)
with col_f1:
    type_filtre = st.selectbox("Voir bilan par", ["Jour", "Mois", "Année", "Tout"], index=0)
with col_f2:
    # FILTRE VENDEUR AUTO
    liste_vendeurs = ["Tous"] + sorted(df["👤 Manager / Vendeur"].astype(str).unique().tolist())
    vendeur_filtre = st.selectbox("Filtrer par vendeur / Code MGR", liste_vendeurs)

if type_filtre == "Jour":
    d = st.date_input("Jour", datetime.now())
    df_f = df[df["date"].dt.date == d]
elif type_filtre == "Mois":
    m = st.selectbox("Mois", range(1,13), index=datetime.now().month-1)
    a = st.number_input("Année", value=2026, key="annee_mois")
    df_f = df[(df["date"].dt.month == m) & (df["date"].dt.year == a)]
elif type_filtre == "Année":
    a = st.number_input("Année", value=2026, key="annee_an")
    df_f = df[df["date"].dt.year == a]
else:
    df_f = df

# Filtre vendeur
if vendeur_filtre != "Tous":
    df_f = df_f[df_f["👤 Manager / Vendeur"] == vendeur_filtre]

st.write(f"**{len(df_f)} ventes trouvées pour ce filtre**")
st.dataframe(df_f, width='stretch')

# --- BILAN SANS BUG + PAR VENDEUR ---
total_vendu = len(df_f)
ca = df_f["Prix de vente (FCFA)"].sum() if "Prix de vente (FCFA)" in df_f.columns else 0
profit = df_f["💰 Profit"].sum() if "💰 Profit" in df_f.columns else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total vendu", total_vendu)
c2.metric("Chiffre", f"{ca:,.0f} F")
c3.metric("Profit", f"{profit:,.0f} F")
c4.metric("Vendeur", vendeur_filtre)

# --- TABLEAU PAR VENDEUR AUTOMATIQUE ---
st.divider()
st.subheader("🏆 Classement par Vendeur (Codes MGR)")
if not df_f.empty:
    classement = df_f.groupby("👤 Manager / Vendeur").agg(
        Ventes=("IMEI","count"),
        CA=("Prix de vente (FCFA)","sum"),
        Profit=("💰 Profit","sum")
    ).reset_index().sort_values("CA", ascending=False)
    st.dataframe(classement, width='stretch')
    
    # Graphique
    st.bar_chart(classement.set_index("👤 Manager / Vendeur")["CA"])

    # Alerte vendeur le plus rentable
    if not classement.empty:
        top = classement.iloc[0]
        st.success(f"🏆 Top vendeur : {top['👤 Manager / Vendeur']} avec {top['CA']:,.0f} F de CA")

def make_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 12, "RAPPORT - MANAGEMENT PHONE SHOP", align="C", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, f"Periode: {type_filtre} - Vendeur: {vendeur_filtre} - {datetime.now().strftime('%d/%m/%Y')}", align="C", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, f"Vendu: {total_vendu} | CA: {ca:,.0f} F | Profit: {profit:,.0f} F", ln=True)
    pdf.ln(5)
    # tableau
    pdf.set_font("Arial", "B", 7)
    cols = [c for c in ["IMEI","Modèle","Marque","Prix de vente (FCFA)","👤 Manager / Vendeur","💰 Profit"] if c in df_f.columns][:6]
    for c in cols:
        pdf.cell(31, 7, c[:15], border=1)
    pdf.ln()
    pdf.set_font("Arial", "", 6)
    for _, r in df_f.head(80).iterrows():
        for c in cols:
            txt = str(r[c])[:15]
            # Eviter caractères unicode qui cassent FPDF
            txt = txt.encode('latin-1', 'ignore').decode('latin-1')
            pdf.cell(31, 6, txt, border=1)
        pdf.ln()
    # Page classement
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Classement Vendeurs", ln=True)
    pdf.set_font("Arial", "", 9)
    for _, r in classement.iterrows():
        pdf.cell(0, 7, f"{r['👤 Manager / Vendeur']} - Ventes: {r['Ventes']} - CA: {r['CA']:,.0f} F - Profit: {r['Profit']:,.0f} F", ln=True)
    return pdf.output(dest='S').encode('latin-1')

if st.button("Générer le PDF", type="primary", width='stretch'):
    pdf_bytes = make_pdf()
    st.download_button("⬇️ TELECHARGER LE PDF", pdf_bytes, f"Rapport_{type_filtre}_{vendeur_filtre}_{datetime.now().date()}.pdf", "application/pdf", width='stretch')
