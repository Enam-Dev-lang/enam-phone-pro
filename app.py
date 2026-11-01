import os
os.makedirs("images_phones", exist_ok=True)

import streamlit as st, os, json

st.set_page_config(page_title="eppro", page_icon="📱", layout="wide")

CONFIG_FILE = "shop_config.json"
WHATSAPP = "+228 72 18 43 97"
MIXX = "+228 91 29 63 08"
FLOOZ = "+228 97 04 42 09"

def check_lic():
    if not os.path.exists(CONFIG_FILE):
        return False
    try:
        with open(CONFIG_FILE,"r",encoding="utf-8") as f:
            return json.load(f).get("licence",{}).get("active",False)
    except:
        return False

if "show_splash" not in st.session_state:
    st.session_state.show_splash = True

# ================= SPLASH PLEIN ECRAN V2 - CENTRE PARFAIT =================
if st.session_state.show_splash:
    st.markdown("""
    <style>
        [data-testid="stSidebar"]{display:none !important;}
        [data-testid="stHeader"]{display:none !important;}
        .block-container{padding-top:2rem !important; max-width:100% !important;}
        div.stButton > button {
            background:#f87171 !important;
            color:white !important;
            font-weight:bold !important;
            font-size:18px !important;
            padding:12px !important;
            border-radius:10px !important;
            border:none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Un seul bloc centré pour logo + bouton
    _, col_centre, _ = st.columns([1, 1.2, 1])
    with col_centre:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        # LOGO CENTRE
        logo_found = False
        for name in ["Logo.png", "logo.png", "Logo.jpg", "logo.jpg"]:
            if os.path.exists(name):
                st.image(name, width='stretch')
                logo_found = True
                break
        if not logo_found:
            st.markdown("<h1 style='text-align:center;'>📱 eppro</h1>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # BOUTON JUSTE EN DESSOUS DU LOGO - MEME COLONNE
        if st.button("▶️ ENTRER DANS eppro", type="primary", width='stretch'):
            st.session_state.show_splash = False
            st.rerun()
        
        st.markdown("<p style='text-align:center; color:#888; margin-top:15px;'>Le logiciel qui fait vendre</p>", unsafe_allow_html=True)

    st.stop()

# ================= APRES LE CLIC - PRESENTATION + MENU =================
is_pro = check_lic()

st.sidebar.title("enam phone pro")
st.sidebar.caption("le logiciel qui fait vendre")
st.sidebar.info(f"📲 WhatsApp\n{WHATSAPP}\n\n💰 Mixx\n{MIXX}\n\n💰 Flooz\n{FLOOZ}")
st.sidebar.divider()
st.sidebar.markdown("👆 **Utilise le menu au dessus pour explorer le logiciel**")

st.markdown("<h1 style='text-align:center;'>📱 enam phone pro</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#666;'>Le logiciel qui fait vendre - Fait à Lomé pour toi</h3>", unsafe_allow_html=True)

if not is_pro:
    st.warning("👋 MODE DECOUVERTE - Limité à 5 téléphones pour tester. Active eppro pour illimité.", icon="🔓")
else:
    st.success("🔒 eppro PRO ACTIVE - Merci Patron !", icon="✅")

st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 🛡️ Anti-Vol Employé\nChaque vendeur a son code `MGR-...`\nTu sais qui a vendu quoi.")
with col2:
    st.markdown("### 👁️ Vitrine Anti-Espion\nClient voit Marque, Modèle, Prix Vente.\nIl ne voit JAMAIS ton bénéfice.")
with col3:
    st.markdown("### 📊 Rapport qui parle\nMeilleur vendeur du mois, CA du jour, PDF pro.")

st.divider()
st.subheader("💰 Sans vs Avec eppro")
c1, c2 = st.columns(2)
with c1:
    st.error("**SANS eppro:**\n- Employé vend et dit pas\n- Client connait ta marge\n- Stock compté à la main jusqu'à 22h")
with c2:
    st.success("**AVEC eppro:**\n- Vente tracée avec code vendeur\n- Bénéfice caché\n- Inventaire auto + backup")

st.info("👈 Utilise le menu à gauche pour explorer : dashboard, Caisse, Inventaire, Rapport, Vitrine...")

st.divider()
st.subheader("🎯 Choisis ton pack")
p1, p2, p3 = st.columns(3)
with p1:
    st.markdown("#### PACK DECOUVERTE\n**0 F**\n- 5 téléphones max\n- Pour tester")
    if st.button("Tester Vitrine", width='stretch', key="vitrine"):
        st.switch_page("pages/Vitrine_Stockage.py")
with p2:
    st.markdown("#### PACK PRO\n**50.000 F / an**\n- Stock ILLIMITÉ\n- PDF\n- Support WhatsApp")
    if st.button("🔑 ACTIVER PRO", type="primary", width='stretch', key="pro"):
        st.switch_page("pages/Activation.py")
with p3:
    st.markdown("#### PACK RESEAU\n**100.000 F / an**\n- 3 boutiques\n- Centralisé")
    if st.button("🔑 ACTIVER PRO MAX", type="primary", width='stretch', key="proMAX"):
        st.switch_page("pages/Activation.py")

st.divider()
st.caption(f"eppro | WhatsApp {WHATSAPP} | Mixx {MIXX} | Flooz {FLOOZ}")