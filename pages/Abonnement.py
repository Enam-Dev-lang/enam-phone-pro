import streamlit as st

st.title("💳 ABONNEMENT ENAM PHONE PRO")
st.markdown("### Dashboard qui fait gagner du temps et de l'argent")
st.divider()

c1, c2 = st.columns(2)
with c1:
    st.subheader("🔥 MENSUEL")
    st.markdown("## 5 000 FCFA / mois")
    st.write("Accès complet + Support WhatsApp")
with c2:
    st.subheader("👑 ANNUEL")
    st.markdown("## 50 000 FCFA / an")
    st.write("2 mois offerts - Support prioritaire")

st.divider()
st.info("**Paiement:**\n\nFlooz: 97 04 42 09\n\nTMoney: 91 29 63 08\n\nNom: ENAM")
st.link_button("💬 Envoyer preuve WhatsApp", "https://wa.me/22897044209", use_container_width=True, type="primary")
st.link_button("⬅️ Retour Dashboard", "https://enam-phone-pro-xscapju7vufnpdztqk6r8w.streamlit.app", use_container_width=True)