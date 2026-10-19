import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Rapport PDF", layout="wide")
st.title("📄 Rapport")

# --- CETTE PARTIE CHERCHE TES DONNEES TOUTE SEULE ---
df = None
# 1. Cherche dans session_state (ton dashboard)
for key in st.session_state.keys():
    if isinstance(st.session_state[key], pd.DataFrame) and len(st.session_state[key]) > 0:
        df = st.session_state[key]
        break

# 2. Sinon cherche un fichier excel/csv dans le projet
if df is None:
    for folder in [".", "data", "datas"]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith((".xlsx", ".csv")):
                    try:
                        path = os.path.join(folder, file)
                        df = pd.read_csv(path) if file.endswith(".csv") else pd.read_excel(path)
                        st.success(f"Données trouvées: {file}")
                        break
                    except: pass

if df is None:
    st.warning("Je ne trouve pas encore tes ventes, j'utilise des données de test. Une fois que tu lances ton dashboard principal avant, je lirai tes vraies ventes.")
    df = pd.DataFrame({
        "date": pd.date_range(start="2026-01-01", periods=50),
        "produit": ["Telephone"]*50,
        "qte": [1,2]*25,
        "stock": [50]*50,
        "prix": [100000]*50
    })

# --- DETECTION AUTO DES COLONNES ---
# Trouve la colonne date, quantité, produit automatiquement
col_date = next((c for c in df.columns if 'date' in c.lower()), df.columns[0])
col_qte = next((c for c in df.columns if 'qte' in c.lower() or 'vendu' in c.lower() or 'quant' in c.lower()), df.columns[1])
col_produit = next((c for c in df.columns if 'produit' in c.lower() or 'article' in c.lower() or 'model' in c.lower()), df.columns[1])

df[col_date] = pd.to_datetime(df[col_date], errors='coerce')
df = df.dropna(subset=[col_date])

# --- FILTRE JOUR / MOIS / AN ---
f1, f2, f3 = st.columns(3)
with f1:
    type_filtre = st.selectbox("Voir bilan par", ["Jour", "Mois", "Année", "Tout"])

if type_filtre == "Jour":
    d = st.date_input("Jour", datetime.now())
    df_f = df[df[col_date].dt.date == d]
elif type_filtre == "Mois":
    c1, c2 = st.columns(2)
    m = c1.selectbox("Mois", range(1,13), index=datetime.now().month-1)
    a = c2.number_input("Année", value=2026)
    df_f = df[(df[col_date].dt.month == m) & (df[col_date].dt.year == a)]
elif type_filtre == "Année":
    a = st.number_input("Année", value=2026)
    df_f = df[df[col_date].dt.year == a]
else:
    df_f = df

st.dataframe(df_f, use_container_width=True)

# --- CALCULS ---
total_vendu = len(df_f) if df_f[col_qte].sum() == 0 else int(df_f[col_qte].sum())
stock_actuel = int(df_f.iloc[-1][col_qte]) if not df_f.empty else 0

# --- PDF ---
def make_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 12, "BILAN ENAM PHONE PRO", align="C", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"ENAM KOSSIVI - {type_filtre} - {datetime.now().strftime('%d/%m/%Y %H:%M')}", align="C", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total Vendu: {total_vendu} | Lignes: {len(df_f)}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 9)
    for col in df_f.columns[:5]:
        pdf.cell(38, 8, str(col)[:15], border=1)
    pdf.ln()
    pdf.set_font("Arial", "", 8)
    for _, r in df_f.head(40).iterrows():
        for col in df_f.columns[:5]:
            pdf.cell(38, 7, str(r[col])[:15], border=1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1')

if st.button("📥 Générer le PDF", type="primary", use_container_width=True):
    pdf_bytes = make_pdf()
    st.download_button("⬇️ TELECHARGER LE RAPPORT PDF", pdf_bytes, f"Rapport_ENAM_{type_filtre}_{datetime.now().date()}.pdf", "application/pdf", use_container_width=True)