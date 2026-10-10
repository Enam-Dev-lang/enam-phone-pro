import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Abonnement PRO - ENAM", layout="centered", page_icon="💳")
FLOOZ = "+228 97 04 42 09"
TMONEY = "+228 91 29 63 08"

st.markdown(f'<div style="text-align:center; padding:20px; background:linear-gradient(90deg,#0A1931,#185ADB); border-radius:15px; color:white;"><h1>📱 MANAGEMENT PHONE SHOP BY ENAM</h1><h3>Dashboard qui fait gagner du temps et de l argent</h3></div>', unsafe_allow_html=True)
st.write("")
st.markdown("### 💼 Choisissez votre plan PRO")

c1,c2 = st.columns(2)
with c1:
    st.markdown("**📅 MOIS**\n\n## 5 000 FCFA\n\n✅ Stock illimité\n✅ Filtre + Manager\n✅ Export Excel")
    st.button("💳 Payer 5 000F")
with c2:
    st.markdown("**🏆 AN - MEILLEUR**\n\n## 50 000 FCFA\n\n✅ Tout Mois\n✅ Logo + Formation\n✅ Economise 10 000F")
    st.button("🏆 Payer 50 000F", type="primary")

st.divider()
st.markdown(f"### 💸 Comment payer ?\n1. Flooz: **{FLOOZ}**\n2. TMoney: **{TMONEY}**\n3. Copie l'ID transaction")

with st.form("pay"):
    nom = st.text_input("🏪 Nom boutique")
    num = st.text_input("📞 Numéro qui a payé")
    idt = st.text_input("🧾 ID Transaction")
    plan = st.selectbox("Plan", ["Mois - 5000 FCFA", "An - 50000 FCFA"])
    if st.form_submit_button("✅ J'ai payé"):
        st.success(f"Merci {nom}! ID {idt} reçu. Licence {plan} en activation.")
        st.markdown(f"[💬 WhatsApp ENAM](https://wa.me/22897044209?text=J'ai%20payé%20{plan}%20ID:{idt})")

st.link_button("💬 Contacter ENAM WhatsApp", "https://wa.me/22897044209", use_container_width=True)