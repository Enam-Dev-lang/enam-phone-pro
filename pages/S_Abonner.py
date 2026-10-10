import streamlit as st
from datetime import datetime

st.set_page_config(page_title="S'Abonner PRO - ENAM", layout="centered", page_icon="💳")

FLOOZ = "+228 97 04 42 09"
TMONEY = "+228 91 29 63 08"

st.markdown("""
<style>
.pricing-card { background: white; border-radius: 20px; padding: 22px; box-shadow: 0 8px 25px rgba(0,0,0,0.12); text-align:left; border:2px solid #eee; height: 320px; }
.pricing-card.best { border-color: #185ADB; background: linear-gradient(180deg, #ffffff 0%, #f0f6ff 100%); }
.price { font-size: 32px; font-weight: 900; color: #0A1931; line-height: 1.1; }
.badge-best { background:#185ADB; color:white; padding:4px 12px; border-radius:20px; font-size:12px; float:right; margin-top:-35px; }
</style>
""", unsafe_allow_html=True)

st.markdown(f'<div style="text-align:center; padding:22px; background:linear-gradient(90deg,#0A1931,#185ADB); border-radius:20px; color:white;"><h2>📱 MANAGEMENT PHONE SHOP BY ENAM</h2><p>Dashboard qui fait gagner du temps et de l argent - Propulsé par Enam</p></div>', unsafe_allow_html=True)
st.write("")
st.markdown("### Choisissez votre abonnement")
st.write("")

c1,c2 = st.columns(2)
with c1:
    st.markdown(f"""
    <div class="pricing-card">
    <div style="font-size:18px;">🗓️ <b>MOIS</b></div>
    <div class="price">5 000 FCFA<br>/ mois</div>
    <hr>
    <div>✅ Stock illimité<br>✅ Filtre + Manager<br>✅ Export Excel</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="pricing-card best">
    <span class="badge-best">BEST</span>
    <div style="font-size:18px;">🏆 <b>AN - MEILLEUR</b></div>
    <div class="price" style="color:#185ADB;">50 000 FCFA<br>/ an</div>
    <div style="background:#d1f0d1; color:#0a7a0a; padding:4px 8px; border-radius:10px; font-size:12px; display:inline-block; margin:6px 0;">Economise 10 000F</div>
    <div>✅ Tout du Mois<br>✅ Logo<br>✅ Formation</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown(f"""
<div style="background:#f5f5f5; padding:20px; border-radius:15px;">
<h3>💵 Comment payer:</h3>
<p>💳 Flooz <b>{FLOOZ}</b><br>💳 TMoney <b>{TMONEY}</b></p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.markdown("### Informations de paiement")

with st.form("paiement_enam"):
    nom_boutique = st.text_input("Nom boutique", placeholder="Ex: Boutique Smartphone Lomé")
    numero_payeur = st.text_input("Numéro qui a payé", placeholder="Ex: +228 97 XX XX XX")
    id_trans = st.text_input("ID Transaction", placeholder="Ex: TRX-123456789")
    plan = st.selectbox("Plan", ["📅 Mensuel - 5 000 FCFA", "🏆 Annuel - 50 000 FCFA (Recommandé)"])
    submit = st.form_submit_button("✅ J'ai payé, Activer", type="primary", use_container_width=True)
    if submit:
        if nom_boutique and numero_payeur and id_trans:
            st.balloons()
            st.success(f"Merci {nom_boutique} ! ID {id_trans} reçu. On active ton plan {plan} en moins de 30 min.")
            st.markdown(f"👉 Clique ici pour confirmer sur WhatsApp: https://wa.me/22897044209?text=Bonjour%20ENAM,%20j'ai%20payé%20{plan}%20ID:{id_trans}%20Boutique:{nom_boutique}%20Num:{numero_payeur}")
        else:
            st.error("Remplis tout ENAM")

st.link_button("💬 Contacter ENAM sur WhatsApp", "https://wa.me/22897044209?text=Bonjour%20ENAM,%20je%20veux%20m'abonner%20PRO", use_container_width=True)
st.caption("Support 7j/7 • Paiement sécurisé • Activation sous 30 min")