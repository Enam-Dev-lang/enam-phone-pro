import streamlit as st
st.set_page_config(page_title="Abonnement ENAM", layout="wide")

# EN-TETE BLEU CYAN ENAM PHONE PRO
st.markdown("""
<div style="
background: linear-gradient(90deg, #06B6D4 0%, #0891B2 50%, #0E7490 100%);
padding: 18px 28px;
border-radius: 14px;
margin-bottom: 22px;
box-shadow: 0 6px 20px rgba(6,182,212,0.35);
display:flex;
align-items:center;
justify-content:space-between;
">
<div style="display:flex; align-items:center; gap:14px;">
<div style="background:white; width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:26px;">📱</div>
<div>
<h1 style="margin:0; color:white; font-size:26px; font-weight:800;">ENAM PHONE PRO</h1>
<p style="margin:2px 0 0 0; color:#E0F2FE; font-size:13px;">Abonnement & Activation Licence</p>
</div>
</div>
<div style="color:white; font-size:13px; background:rgba(255,255,255,0.18); padding:6px 14px; border-radius:20px;">
💳 Abonnement
</div>
</div>
""", unsafe_allow_html=True)

# CORRECTION FOND + CARTES
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
background: #f0f2f5 !important;
}
div[data-testid="stColumn"] > div {
background: white !important;
border-radius: 16px !important;
padding: 20px !important;
box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
border: 1px solid #e5e7eb !important;
height: auto !important;
min-height: 420px !important;
overflow: visible !important;
}
div[data-testid="stColumn"] p, div[data-testid="stColumn"] h2, div[data-testid="stColumn"] h3, div[data-testid="stColumn"] li {
color: #111827 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align:center; color:#111827;'>Choisissez votre plan</h3>", unsafe_allow_html=True)
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🌱 GRATUIT")
    st.markdown("**0 F / mois**")
    st.markdown("✅ 10 appareils max")
    st.markdown("✅ Gestion stock de base")
    st.markdown("❌ Pas de facture PDF")
    st.info("Pour tester")
    if st.button("Commencer gratuit", use_container_width=True):
        st.session_state['plan_choisi'] = "GRATUIT"
        st.success("Mode gratuit activé")

with col2:
    st.markdown("### 🔥 MENSUEL ⭐")
    st.markdown("**5 000 F / mois**")
    st.caption("166F / jour - POPULAIRE")
    st.markdown("✅ Appareils illimités")
    st.markdown("✅ Facture PRO + PDF")
    st.markdown("✅ Support WhatsApp 24h")
    if st.button("S'abonner 5 000F", type="primary", use_container_width=True):
        st.session_state['plan_choisi'] = "MENSUEL 5000F"
        st.warning("Voir paiement en bas")

with col3:
    st.markdown("### 👑 ANNUEL")
    st.markdown("**50 000 F / an**")
    st.caption("2 mois offerts")
    st.markdown("👑 Tout mensuel +")
    st.markdown("🎓 Formation vente")
    st.markdown("🏆 Badge certifié")
    st.markdown("**Economisez 10 000F**")
    if st.button("S'abonner Annuel", use_container_width=True):
        st.session_state['plan_choisi'] = "ANNUEL 50000F"
        st.warning("Voir paiement en bas")

st.write("")

st.markdown("""
<div style="background:#1e40af; color:white; padding:14px; border-radius:10px; text-align:center; font-weight:600;">
💳 PAIEMENT - FLOOZ / MIXX: MIXX: 91 29 63 08 (ENAM KOSSIVI) | FLOOZ: 97 04 42 09 (ENAM KOSSIVI)
</div>
""", unsafe_allow_html=True)

# AMELIORATION : WhatsApp avec le plan choisi automatiquement
plan_choisi = st.session_state.get('plan_choisi', 'MENSUEL ou ANNUEL')
if plan_choisi == "GRATUIT":
    wa_text = "Bonjour ENAM, je veux tester l'offre GRATUITE ENAM PHONE PRO"
else:
    wa_text = f"Bonjour ENAM, j'ai paye pour {plan_choisi} ENAM PHONE PRO. Voici ma preuve de paiement Mixx/Flooz"

wa_text_encoded = wa_text.replace(" ", "%20").replace("\n", "%0A")

st.markdown(f"""
<a href="https://wa.me/22872184397?text={wa_text_encoded}" target="_blank" style="text-decoration:none;">
<div style="background:#25D366; color:white; padding:14px; border-radius:10px; text-align:center; font-weight:700; margin-top:12px; font-size:16px;">
📲 ENVOYER PREUVE WHATSAPP - ACTIVATION 5 MIN ({plan_choisi})
</div>
</a>
""", unsafe_allow_html=True)