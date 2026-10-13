import streamlit as st
st.set_page_config(page_title="Abonnement", layout="wide")

st.markdown("""
<style>
.box
  box {background: linear-gradient(135deg,#6a5af9,#a46bff); 
  padding:30px;
  border-radius:18px; 
  color:white; 
  text-align:center;
  }
.card {
  background:white; 
  border-radius:16px; 
  padding:22px; 
  border:1px solid #eee; 
  box-shadow:0 6px 20px rgba(0,0,0,0.07);
  }
.price {
  font-size:36px; 
  font-weight:900;
  }
</style>
<div class="box"><h1>💎 ENAM PHONE PRO</h1><p>Dashboard qui te fait gagner temps & argent à Lomé</p></div><br>
""", unsafe_allow_html=True)

a,b,c = st.columns(3)
with a: st.markdown('<div class="card"><h3>🌱 GRATUIT</h3><div class="price">0 F</div>3 jours<br><br>✅ Stock illimité<br>✅ Bénéfice auto<br><br></div>', unsafe_allow_html=True)
with b: st.markdown('<div class="card" style="border:2.5px solid #6a5af9;"><h3>🔥 MENSUEL ⭐</h3><div class="price">5 000 F</div>/ mois<br><p style="color:#6a5af9;font-weight:700;">166F / jour</p><hr>🚀 Illimité<br>💰 Bénéfice auto<br>💬 Support WhatsApp<br><br><b>LE PLUS CHOISI</b></div>', unsafe_allow_html=True)
with c: st.markdown('<div class="card"><h3>👑 ANNUEL</h3><div class="price">50 000 F</div>/ an<br><p style="color:green;font-weight:700;">2 mois offerts</p><hr>👑 Tout + Formation<br>🏆 Groupe VIP<br><br><b>Économise 10 000F</b></div>', unsafe_allow_html=True)

st.write("")
st.markdown('<div style="background:#f0f7ff; border-left:5px solid #2b7cff; padding:18px; border-radius:12px;"><b>💳 PAIEMENT</b><br><br>🟡 FLOOZ / MIXX: <b>97 04 42 09</b> (ENAM LANG) | 🔵 T-MONEY: <b>91 29 63 08</b></div>', unsafe_allow_html=True)
st.link_button("📲 ENVOYER PREUVE WHATSAPP - ACTIVATION 5 MIN", "https://wa.me/22897044209", type="primary", use_container_width=True)