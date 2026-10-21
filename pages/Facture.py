
import streamlit as st
import datetime
import json
import os
import base64
from io import BytesIO

try:
    from fpdf import FPDF
    HAS_PDF = True
except:
    HAS_PDF = False

st.set_page_config(page_title="Facture PRO + PDF", layout="centered")

def get_logo_path():
    return "boutique_logo.png" if os.path.exists("boutique_logo.png") else None

def get_logo_html():
    path = get_logo_path()
    if path:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            return f'<img src="data:image/png;base64,{b64}" style="width:80px;height:80px;object-fit:contain;border-radius:12px;background:white;padding:4px;">'
    return '<div style="width:80px;height:80px;border:2px dashed #6366f1;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#6366f1;font-size:11px;text-align:center;">LOGO<br>CLIENT</div>'

if "boutique_nom" not in st.session_state:
    st.session_state.boutique_nom = "ENAM PHONE PRO"
    st.session_state.boutique_tel = "90 12 34 56"
    st.session_state.boutique_adresse = "Lome, Togo - Grand Marche"
    st.session_state.boutique_email = "contact@enamphone.tg"

st.title("🧾 Facture PRO + PDF")

with st.expander("⚙️ Configurer boutique"):
    nom = st.text_input("Nom", st.session_state.boutique_nom)
    tel = st.text_input("Tel", st.session_state.boutique_tel)
    adresse = st.text_input("Adresse", st.session_state.boutique_adresse)
    email = st.text_input("Email", st.session_state.boutique_email)
    logo = st.file_uploader("Logo boutique (laisser vide si client n'a pas encore)", type=["png","jpg","jpeg"])
    if logo:
        with open("boutique_logo.png","wb") as f:
            f.write(logo.getbuffer())
        st.image("boutique_logo.png", width=100)
    if st.button("Sauver"):
        st.session_state.boutique_nom = nom
        st.session_state.boutique_tel = tel
        st.session_state.boutique_adresse = adresse
        st.session_state.boutique_email = email
        st.rerun()

st.divider()
c1,c2 = st.columns(2)
with c1:
    client_nom = st.text_input("Nom Client", "M. Kodjo")
    client_tel = st.text_input("Tel Client", "90 12 34 56")
with c2:
    agent = st.text_input("Agent / Vendeur (Exécuté par)", "Paul")
    date_fact = st.date_input("Date", datetime.date.today())

if os.path.exists("factures.json"):
    try:
        with open("factures.json","r") as f:
            num = len(json.load(f)) + 1
    except:
        num = 1
else:
    num = 1
code_facture = f"FAC-{datetime.date.today().year}-{num:04d}"
st.info(f"Code: **{code_facture}** | Place logo vide = client ajoutera son logo après achat")

if "lignes" not in st.session_state:
    st.session_state.lignes = [{"designation":"iPhone 13 128Go Noir","imei":"352123456789","prix":250000,"qte":1}]

for i,l in enumerate(st.session_state.lignes):
    cc1,cc2,cc3,cc4 = st.columns([3,2,2,1])
    with cc1:
        l["designation"] = st.text_input(f"Des {i+1}", l["designation"], key=f"d{i}", label_visibility="collapsed", placeholder="Designation")
    with cc2:
        l["imei"] = st.text_input(f"Imei {i+1}", l["imei"], key=f"im{i}", label_visibility="collapsed", placeholder="IMEI")
    with cc3:
        l["prix"] = st.number_input(f"Prix {i+1}", value=l["prix"], key=f"p{i}", label_visibility="collapsed", step=1000)
    with cc4:
        l["qte"] = st.number_input(f"Qte {i+1}", value=l["qte"], min_value=1, key=f"q{i}", label_visibility="collapsed")

if st.button("➕ Ajouter article"):
    st.session_state.lignes.append({"designation":"","imei":"","prix":0,"qte":1})
    st.rerun()

total = sum(x["prix"]*x["qte"] for x in st.session_state.lignes)

# --- HTML APERCU ---
rows = ""
for idx, l in enumerate(st.session_state.lignes, 1):
    if not l["designation"]:
        continue
    rows += f"""
    <tr style="border-bottom:1px solid #f3f4f6;">
      <td style="padding:14px 0; color:#9ca3af;">{idx:02d}</td>
      <td style="padding:14px 0;"><div style="font-weight:600;">{l['designation']}</div><div style="font-size:11px; color:#6b7280; font-family:monospace;">IMEI: {l['imei'] or '-'}</div></td>
      <td style="padding:14px 0; text-align:center; font-weight:600;">{l['qte']}</td>
      <td style="padding:14px 0; text-align:right; font-weight:600;">{l['prix']*l['qte']:,} F</td>
    </tr>
    """
logo_html = get_logo_html()
final_html = f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<div id="facture-print" style="font-family:Inter,sans-serif; background:white; color:#111827; border-radius:16px; box-shadow:0 10px 30px rgba(0,0,0,0.08); border:1px solid #e5e7eb; overflow:hidden; max-width:750px; margin:auto;">
  <div style="background:linear-gradient(135deg,#111827,#1f2937); color:white; padding:28px 32px; display:flex; justify-content:space-between; align-items:center;">
    <div style="display:flex; gap:18px; align-items:center;">{logo_html}<div><h1 style="margin:0; font-size:22px; font-weight:700;">{st.session_state.boutique_nom}</h1><p style="margin:4px 0 0 0; font-size:13px; opacity:0.8;">{st.session_state.boutique_adresse}</p><p style="margin:2px 0 0 0; font-size:13px; opacity:0.8;">{st.session_state.boutique_tel} - {st.session_state.boutique_email}</p></div></div>
    <div style="text-align:right;"><p style="margin:0; font-size:11px; letter-spacing:2px; opacity:0.6; font-weight:600;">FACTURE</p><p style="margin:6px 0 0 0; font-size:20px; font-weight:700; font-family:monospace;">{code_facture}</p><p style="margin:4px 0 0 0; font-size:12px; opacity:0.7;">{date_fact.strftime('%d %b %Y')}</p></div>
  </div>
  <div style="padding:24px 32px; display:flex; justify-content:space-between; background:#f9fafb; border-bottom:1px solid #e5e7eb;">
    <div><p style="margin:0 0 6px 0; font-size:10px; letter-spacing:1.5px; color:#6b7280; font-weight:600;">FACTURE A</p><p style="margin:0; font-size:15px; font-weight:600;">{client_nom}</p><p style="margin:2px 0 0 0; font-size:13px; color:#4b5563;">{client_tel}</p></div>
    <div style="text-align:right;"><p style="margin:0 0 6px 0; font-size:10px; letter-spacing:1.5px; color:#6b7280; font-weight:600;">VENDU PAR</p><p style="margin:0; font-size:14px; font-weight:600;">{agent}</p><p style="margin:2px 0 0 0; font-size:12px; color:#6b7280; font-family:monospace;">Execute par: {agent}</p></div>
  </div>
  <div style="padding:0 32px;">
    <table style="width:100%; border-collapse:collapse; margin-top:20px; font-size:13px;">
      <thead><tr style="text-align:left; color:#6b7280; font-size:11px; border-bottom:1px solid #e5e7eb;"><th style="padding:12px 0;">#</th><th style="padding:12px 0;">DESIGNATION & IMEI</th><th style="padding:12px 0; text-align:center;">QTE</th><th style="padding:12px 0; text-align:right;">PRIX</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <div style="display:flex; justify-content:flex-end; margin-top:20px;"><div style="width:260px; background:#111827; color:white; border-radius:12px; padding:16px 20px; display:flex; justify-content:space-between;"><span style="font-size:11px; opacity:0.7;">TOTAL</span><span style="font-size:18px; font-weight:700; font-family:monospace;">{total:,} F</span></div></div>
    <div style="display:flex; justify-content:space-between; margin-top:48px; padding-top:24px; border-top:1px dashed #d1d5db;"><div style="text-align:center; width:45%;"><p style="margin:0 0 40px 0; font-size:10px; color:#9ca3af;">SIGNATURE CLIENT</p><div style="border-top:1px solid #111827; width:80%; margin:auto;"></div></div><div style="text-align:center; width:45%;"><p style="margin:0 0 8px 0; font-size:10px; color:#9ca3af;">POUR {st.session_state.boutique_nom}</p><p style="margin:0 0 30px 0; font-size:12px;">Agent: {agent}</p><div style="border-top:1px solid #111827; width:80%; margin:auto;"></div><p style="margin:6px 0 0 0; font-size:10px; color:#9ca3af;">Cachet & Signature</p></div></div>
    <div style="text-align:center; margin-top:32px; padding:14px; background:#f9fafb; font-size:10px; color:#9ca3af;">Merci - {code_facture}</div>
  </div>
</div>
"""
st.markdown(final_html, unsafe_allow_html=True)

# --- GENERATION PDF ---
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    # Header noir
    pdf.set_fill_color(17,24,39)
    pdf.rect(0,0,210,45, 'F')
    pdf.set_y(8)
    # Logo
    logo_path = get_logo_path()
    if logo_path:
        try:
            pdf.image(logo_path, x=10, y=8, w=20, h=20)
        except:
            pass
    # Boutique
    pdf.set_xy(35, 10)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(255,255,255)
    pdf.cell(0, 7, st.session_state.boutique_nom, ln=False)
    pdf.set_xy(35, 18)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(200,200,200)
    pdf.cell(0, 5, f"{st.session_state.boutique_adresse} | {st.session_state.boutique_tel}", ln=False)
    # Facture droite
    pdf.set_xy(130, 10)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(180,180,255)
    pdf.cell(0, 5, "FACTURE", align="R")
    pdf.set_xy(130, 16)
    pdf.set_font("Courier", "B", 13)
    pdf.set_text_color(255,255,255)
    pdf.cell(0, 6, code_facture, align="R")
    pdf.set_xy(130, 24)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, str(date_fact), align="R")

    pdf.set_y(50)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(100,100,100)
    pdf.cell(90, 5, "FACTURE A", ln=False)
    pdf.cell(0, 5, "VENDU PAR", align="R", ln=True)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0,0,0)
    pdf.cell(90, 6, client_nom, ln=False)
    pdf.cell(0, 6, agent, align="R", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80,80,80)
    pdf.cell(90, 5, client_tel, ln=False)
    pdf.cell(0, 5, f"Execute par: {agent}", align="R", ln=True)

    pdf.ln(8)
    # Tableau header
    pdf.set_fill_color(17,24,39)
    pdf.set_text_color(255,255,255)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(10, 8, "#", fill=True)
    pdf.cell(90, 8, "DESIGNATION & IMEI", fill=True)
    pdf.cell(20, 8, "QTE", fill=True, align="C")
    pdf.cell(0, 8, "PRIX", fill=True, align="R")
    pdf.ln()
    # Lignes
    pdf.set_text_color(0,0,0)
    pdf.set_font("Helvetica", "", 9)
    for idx, l in enumerate(st.session_state.lignes, 1):
        if not l["designation"]:
            continue
        h = 12
        pdf.cell(10, h, f"{idx:02d}", border="B")
        txt = f"{l['designation']} (IMEI:{l['imei']})"
        pdf.cell(90, h, txt[:55], border="B")
        pdf.cell(20, h, str(l["qte"]), border="B", align="C")
        pdf.cell(0, h, f"{l['prix']*l['qte']:,} F", border="B", align="R", ln=True)
    # Total
    pdf.ln(5)
    pdf.set_x(120)
    pdf.set_fill_color(17,24,39)
    pdf.set_text_color(255,255,255)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(80, 12, f"TOTAL: {total:,} F CFA", fill=True, align="C")

    pdf.ln(20)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100,100,100)
    pdf.cell(90, 5, "Signature Client", align="C")
    pdf.cell(0, 5, f"Pour {st.session_state.boutique_nom} - Agent: {agent}", align="C", ln=True)
    pdf.ln(10)
    pdf.set_draw_color(0,0,0)
    pdf.line(15, pdf.get_y(), 85, pdf.get_y())
    pdf.line(125, pdf.get_y(), 195, pdf.get_y())

    return pdf.output()

# --- BOUTONS ---
st.divider()
col_pdf, col_print = st.columns(2)

with col_pdf:
    if HAS_PDF:
        if st.button("📄 Générer PDF", type="primary", use_container_width=True):
            pdf_bytes = create_pdf()
            st.session_state['pdf_bytes'] = pdf_bytes
            st.success("PDF prêt !")
        if 'pdf_bytes' in st.session_state:
            st.download_button(
                label="⬇️ Télécharger Facture PDF",
                data=st.session_state['pdf_bytes'],
                file_name=f"{code_facture}_{client_nom}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
    else:
        st.error("Ajoute fpdf2 dans requirements.txt")

with col_print:
    st.markdown("""
    <button onclick="window.print()" style="width:100%; padding:12px; background:white; border:1px solid #111827; border-radius:8px; font-weight:600; cursor:pointer;">🖨️ Imprimer (Ctrl+P)</button>
    """, unsafe_allow_html=True)
    st.caption("Le bouton imprime la page avec logo + facture PRO")

if st.button("💾 Enregistrer facture", use_container_width=True):
    data = {"code":code_facture,"date":str(date_fact),"client":client_nom,"client_tel":client_tel,"agent":agent,"boutique":st.session_state.boutique_nom,"lignes":st.session_state.lignes,"total":total}
    all_f = []
    if os.path.exists("factures.json"):
        try:
            with open("factures.json","r") as f:
                all_f = json.load(f)
        except:
            all_f = []
    all_f.append(data)
    with open("factures.json","w") as f:
        json.dump(all_f,f,indent=2,ensure_ascii=False)
    st.success("Enregistrée")
    st.balloons()