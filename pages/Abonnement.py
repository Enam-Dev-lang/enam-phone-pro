import streamlit as st
st.set_page_config(page_title="Abonnement ENAM", layout="wide")

st.markdown("""
<style>
.header {
background: linear-gradient(90deg, #6a5af9 0%, #a46bff 100%);
padding: 35px; border-radius: 18px; color: white; text-align: center; margin-bottom: 25px;
}
.header h1 { color: white !important; margin:0; }
.card { background: white; border: 1px solid #e9e9e9; border-radius: 16px; padding: 22px; box-shadow: 0 8px 25px rgba(0,0,0,0.06); height: 420px; }
.card-popular { border: 2.5px solid #6a5af9 !important; }
.price { font-size: 34px; font-weight: 900; color: #111; }
.badge { background: #6a5af9; color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; }
</style>
<div class="header">
<h1>💎 ENAM PHONE PRO</h1>
<p>Tableau de bord qui te fait gagner temps & argent à Lomé</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="card">
    <h3>🌱 GRATUIT</h3>
    <div class="price">0 F</div>
    <small>3 jours d'essai</small><br><br>
    ✅ Stock illimité<br>
    ✅ Bénéfice auto<br><br><br>
    <b>Pour tester</b>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="card card-popular">
    <h3>🔥 MENSUEL <span class="badge">⭐ POPULAIRE</span></h3>
    <div class="price">5 000 F</div>
    <small>/ mois - <b style="color:#6a5af9;">166F / jour</b></small><br><br>
    🚀 Stock Illimité<br>
    💰 Bénéfice auto<br>
    💬 Support WhatsApp<br><br>
    <b style="color:#6a5af9;">LE PLUS CHOISI</b>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="card">
    <h3>👑 ANNUEL</h3>
    <div class="price">50 000 F</div>
    <small>/ an - <b style="color:green;">2 mois offerts</b></small><br><br>
    👑 Tout illimité<br>
    🎓 Formation incluse<br>
    🏆 Groupe VIP<br><br>
    <b>Économisez 10 000F</b>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# --- MODIFICATION 1 : Numéro de paiement ---
st.info("💳 **PAIEMENT** - FLOOZ / MIXX(T-money) : MIXX: **91 29 63 08(ENAM KOSSIVI)** | FLOOZ: **97 04 42 09(ENAM KOSSIVI)**")

# --- MODIFICATION 2 : Numéro WhatsApp qui reçoit les captures ---
st.link_button("📲 ENVOYER PREUVE WHATSAPP - ACTIVATION 5 MIN", "https://wa.me/22891296308", type="primary", use_container_width=True)