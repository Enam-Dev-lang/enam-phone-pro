# pages/Vitrine_Stockage.py - VITRINE GLOBALE CORRIGEE - MODE CLIENT SECURISE
import streamlit as st, os, json, pandas as pd
from PIL import Image

st.set_page_config(page_title="Vitrine Stockage", page_icon="🖼️", layout="wide")

STOCK_FILE = "stock.xlsx"
IMAGE_FOLDER = "images_phones"
IMAGE_MAP = "images_map.json"

os.makedirs(IMAGE_FOLDER, exist_ok=True)

def load_stock():
    if not os.path.exists(STOCK_FILE):
        return pd.DataFrame(columns=["IMEI","Modèle","Marque","Prix Achat (FCFA)","Prix de vente (FCFA)","📦 Statut"])
    try:
        return pd.read_excel(STOCK_FILE)
    except:
        return pd.DataFrame()

def load_map():
    if os.path.exists(IMAGE_MAP):
        try:
            with open(IMAGE_MAP, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_map(data):
    with open(IMAGE_MAP, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# EN-TETE
st.markdown("""
<div style="background: linear-gradient(90deg, #111827, #06B6D4); padding:18px 28px; border-radius:14px; margin-bottom:20px;">
<h1 style="margin:0; color:white;">🖼️ VITRINE GLOBALE - Stock Magasin</h1>
<p style="margin:0; color:#E0F2FE;">Présente tes téléphones à la clientèle avec photos</p>
</div>
""", unsafe_allow_html=True)

df = load_stock()
image_map = load_map()

# MODE CLIENT
col_vide, col_client = st.columns([4, 1])
with col_client: 
    mode_client = st.toggle("👁️ Mode Client", value=False)

if mode_client:
    st.warning("🔒 Mode Client ACTIVÉ")
else:
    st.info("🔓 Mode Patron")

# RECHERCHE
search = st.text_input("🔍 Rechercher Marque / Modèle / IMEI", placeholder="Ex: iPhone 13, Samsung, 35...")
if not df.empty and search:
    df = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]

# TABS
tab_vitrine, tab_upload = st.tabs(["🏬 Vitrine Magasin", "📤 Ajouter Photos"])

with tab_upload:
    st.subheader("Uploader la photo du téléphone")
    if df.empty:
        st.warning("Stock vide - Va dans Ajout au stock d'abord")
    else:
        imei_select = st.selectbox("Choisir IMEI / Modèle", df.apply(lambda x: f"{x['IMEI']} - {x['Modèle']}", axis=1).tolist())
        if imei_select:
            vrai_imei = imei_select.split(" - ")[0]
            uploaded = st.file_uploader("Photo du téléphone", type=["jpg","png","jpeg"], key="up")
            if uploaded:
                ext = uploaded.name.split(".")[-1]
                path = os.path.join(IMAGE_FOLDER, f"{vrai_imei}.{ext}")
                with open(path, "wb") as f:
                    f.write(uploaded.getbuffer())
                image_map[vrai_imei] = path
                save_map(image_map)
                st.success(f"Photo ajoutée pour {vrai_imei}")
                st.image(uploaded, width=200)

with tab_vitrine:
    if df.empty:
        st.info("Aucun téléphone en stock")
    else:
        cols = st.columns(3)
        for idx, row in df.iterrows():
            col = cols[idx % 3]
            imei = str(row["IMEI"])
            img_path = image_map.get(imei)
            
            with col:
                with st.container(border=True):
                    if img_path and os.path.exists(img_path):
                        st.image(img_path, use_container_width=True)
                    else:
                        st.markdown(f"""<div style="height:180px; background:#F3F4F6; display:flex; align-items:center; justify-content:center; border-radius:10px;"><span style="font-size:50px;">📱</span></div>""", unsafe_allow_html=True)
                        st.caption("Pas de photo")
                    
                    st.markdown(f"**{row.get('Marque','')} {row.get('Modèle','')}**")
                    st.caption(f"IMEI: {imei[:15]}...")
                    
                    # --- CORRECTION ICI : PRIX ACHAT CACHE EN MODE CLIENT ---
                    if not mode_client:
                        st.write(f"🛒 Achat: {row.get('Prix Achat (FCFA)',0):,.0f} FCFA")
                        st.write(f"💹 Profit: {row.get('💰 Profit',0):,.0f} FCFA")
                    # --------------------------------------------------------
                    
                    st.markdown(f"### 💰 {row.get('Prix de vente (FCFA)',0):,.0f} FCFA")
                    
                    statut = row.get("📦 Statut","En Stock")
                    if statut == "En Stock":
                        st.success(f"✅ {statut}")
                    else:
                        st.error(f"❌ {statut}")
                    
                    if st.button("📄 Voir détails", key=f"detail_{imei}", use_container_width=True):
                        if mode_client:
                            # MODE CLIENT SECURISE
                            safe_data = {
                                "Marque": row.get("Marque",""),
                                "Modèle": row.get("Modèle",""),
                                "Prix de vente (FCFA)": f"{row.get('Prix de vente (FCFA)',0):,.0f} FCFA",
                                "Statut": row.get("📦 Statut","En Stock"),
                                "Garantie": "6 mois ENAM PHONE PRO"
                            }
                            st.json(safe_data)
                        else:
                            # MODE PATRON COMPLET
                            st.json(row.to_dict())

st.divider()
st.markdown("💡 Astuce: Active Mode Client quand un client regarde. Désactive-le quand tu es seul.")
