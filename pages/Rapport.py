import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Rapport", layout="wide")
st.title("Rapport")

FICHIER_STOCK = "stock.xlsx"

# --- LECTURE DIRECTE DE TON FICHIER ---
if not os.path.exists(FICHIER_STOCK):
    st.warning("stock.xlsx n'existe pas encore. Ajoute un téléphone dans le dashboard phone puis reviens.")
    st.stop()

try:
    df = pd.read_excel(FICHIER_STOCK)
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

# --- FILTRE ---
type_filtre = st.selectbox("Voir bilan par", ["Jour", "Mois", "Année", "Tout"], index=0)

if type_filtre == "Jour":
    d = st.date_input("Jour", datetime.now())
    df_f = df[df["date"].dt.date == d]
elif type_filtre == "Mois":
    m = st.selectbox("Mois", range(1,13), index=datetime.now().month-1)
    a = st.number_input("Année", value=2026)
    df_f = df[(df["date"].dt.month == m) & (df["date"].dt.year == a)]
elif type_filtre == "Année":
    a = st.number_input("Année", value=2026)
    df_f = df[df["date"].dt.year == a]
else:
    df_f = df

st.write(f"**{len(df_f)} ventes trouvées pour ce filtre**")
st.dataframe(df_f, use_container_width=True)

# --- BILAN SANS BUG ---
total_vendu = len(df_f)
ca = df_f["Prix de vente (FCFA)"].sum() if "Prix de vente (FCFA)" in df_f.columns else 0
profit = df_f["💰 Profit"].sum() if "💰 Profit" in df_f.columns else 0

st.metric("Total vendu", total_vendu)
st.metric("Chiffre", f"{ca:,.0f} F")
st.metric("Profit", f"{profit:,.0f} F")

def make_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 12, "RAPPORT - MANAGEMENT PHONE SHOP", align="C", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, f"Periode: {type_filtre} - {datetime.now().strftime('%d/%m/%Y')}", align="C", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, f"Vendu: {total_vendu} | CA: {ca:,.0f} F | Profit: {profit:,.0f} F", ln=True)
    pdf.ln(5)
    # tableau
    pdf.set_font("Arial", "B", 7)
    cols = [c for c in ["IMEI","Modèle","Marque","Prix de vente (FCFA)","📦 Statut","💰 Profit"] if c in df_f.columns][:6]
    for c in cols: pdf.cell(31, 7, c[:15], border=1)
    pdf.ln()
    pdf.set_font("Arial", "", 6)
    for _, r in df_f.head(50).iterrows():
        for c in cols: pdf.cell(31, 6, str(r[c])[:15], border=1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1')

if st.button("Générer le PDF", type="primary", use_container_width=True):
    pdf_bytes = make_pdf()
    st.download_button("⬇️ TELECHARGER LE PDF", pdf_bytes, f"Rapport_{type_filtre}_{datetime.now().date()}.pdf", "application/pdf", use_container_width=True)