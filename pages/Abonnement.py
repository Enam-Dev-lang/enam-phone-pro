import streamlit as st

st.set_page_config(page_title="Abonnement - ENAM PHONE", layout="centered")

st.title("💳 ABONNEMENT ENAM PHONE PRO")
st.markdown("### Dashboard qui fait gagner du temps et de l'argent - Propulsé par Enam")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔥 OFFRE MENSUELLE")
    st.markdown("## 5 000 FCFA / mois")
    st.write("Accès complet au Dashboard")
    st.write("Support WhatsApp")
    st.write("Mises à jour gratuites")
    if st.button("S'abonner 5000F / mois", use_container_width=True):
        st.success("Payez par Flooz ou TMoney ci-dessous 👇")

with col2:
    st.markdown("#### 👑 OFFRE ANNUELLE - 2 MOIS OFFERTS")
    st.markdown("## 50 000 FCFA / an")
    st.write("Tout l'offre mensuelle")
    st.write("Économisez 10 000 F")
    st.write("Support prioritaire")
    if st.button("S'abonner 50 000F / an", type="primary", use_container_width=True):
        st.success("Payez par Flooz ou TMoney ci-dessous 👇")

st.divider()
st.markdown("### 📲 PAIEMENT MOBILE MONEY")

st.info("""
**Flooz : 97 04 42 09**\n
**TMoney : 91 29 63 08**\n
Nom : ENAM
""")

st.warning("Après paiement, envoyez la capture sur WhatsApp pour activation immédiate.")

st.link_button("💬 Envoyer preuve sur WhatsApp", "https://wa.me/22897044209", use_container_width=True)
st.link_button("⬅️ Retour au Dashboard", "https://enam-phone-pro-xscapju7vufnpdztqk6r8w.streamlit.app", use_container_width=True)