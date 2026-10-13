import streamlit as st

st.set_page_config(page_title="Abonnement - ENAM PHONE PRO", layout="wide")

# --- DESIGN CSS ULTRA PRO ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
* {font-family: 'Outfit', sans-serif;}
.header-gradient {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 40px; border-radius: 20px; color: white; text-align: center; margin-bottom: 30px;
}
.pricing-card {
    background: white; border-radius: 20px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    border: 2px solid #f0f0f0; transition: 0.3s; height: 100%;
}
.pricing-card:hover {transform: translateY(-10px); box-shadow: 0 20px 60px rgba(0,0,0,0.15);}
.popular {border: 2.5px solid #667eea; position: relative;}
.badge-pop {
    background: linear-gradient(135deg, #ff6a00, #ee0979); color: white; padding: 6px 18px;
    border-radius: 20px; font-size: 12px; font-weight: 900; position: absolute; top: -15px; right: 20px;
}
.price {font-size: 42px; font-weight: 900; color: #1a1a1a;}
.price span {font-size: 16px; font-weight: 400; color: #888;}
.btn-pay {
    background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 15px;
    border-radius: 12px; text-align: center; font-weight: 800; font-size: 16px; margin-top: 20px;
}
.payment-box {
    background: linear-gradient(135deg, #e0f2fe, #dbeafe); border-radius: 16px; padding: 25px;
    border-left: 6px solid #3b82f6;
}
.feature {display: flex; align-items: center; margin: 10px 0;}
.feature span {margin-right: 10px; font-size: 18px;}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="header-gradient">
    <h1 style="font-size:50px; font-weight:900; margin:0;">💎 ENAM PHONE PRO</h1>
    <p style="font-size:20px; opacity:0.9; margin-top:10px;">Le Dashboard qui transforme ton petit shop en entreprise qui encaisse</p>
    <p style="margin-top:15px; background:rgba(255,255,255,0.2); display:inline-block; padding:8px 20px; border-radius:20px;">🔥 Déjà 47 boutiques à Lomé nous font confiance</p>
</div>
""", unsafe_allow_html=True)

# --- PRICING ---
col1, col2, col3 = st.columns([1,1,1], gap="large")

with col1:
    st.markdown("""
    <div class="pricing-card">
        <h3>🌱 ESSAI GRATUIT</h3>
        <div class="price">0 F <span>/ 3 jours</span></div>
        <p style="color:#666;">Pour tester sans risque</p>
        <hr>
        <div class="feature"><span>✅</span> Gestion stock illimité</div>
        <div class="feature"><span>✅</span> Calcul bénéfice auto</div>
        <div class="feature"><span>✅</span> 4 appareils max</div>
        <div class="feature"><span>❌</span> Pas de support prio</div>
        <div style="margin-top:30px; background:#f3f4f6; padding:12px; border-radius:10px; text-align:center; font-weight:700;">Déjà actif</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="pricing-card popular">
        <div class="badge-pop">⭐ LE PLUS CHOISI</div>
        <h3>🔥 MENSUEL PRO</h3>
        <div class="price">5 000 F <span>/ mois</span></div>
        <p style="color:#667eea; font-weight:700;">Soit 166F / jour seulement</p>
        <hr>
        <div class="feature"><span>🚀</span> <b>Stock & Ventes illimités</b></div>
        <div class="feature"><span>💰</span> <b>Bénéfice / Jour / Mois auto</b></div>
        <div class="feature"><span>📊</span> <b>Graphiques & Alertes</b></div>
        <div class="feature"><span>💬</span> <b>Support WhatsApp 7j/7</b></div>
        <div class="feature"><span>⚡</span> <b>Accès immédiat après paiement</b></div>
        <div class="btn-pay">Choisir ce plan</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="pricing-card">
        <h3>👑 ANNUEL VIP</h3>
        <div class="price">50 000 F <span>/ an</span></div>
        <p style="color:#10b981; font-weight:700;">Tu économises 10 000F (2 mois OFFERTS)</p>
        <hr>
        <div class="feature"><span>👑</span> <b>Tout du plan Mensuel +</b></div>
        <div class="feature"><span>🎁</span> <b>Formation vente incluse</b></div>
        <div class="feature"><span>🔔</span> <b>Alertes ruptures par SMS</b></div>
        <div class="feature"><span>🏆</span> <b>Groupe VIP revendeurs Lomé</b></div>
        <div class="feature"><span>🛡️</span> <b>Assistance prioritaire</b></div>
        <div style="margin-top:20px; background:linear-gradient(135deg, #10b981, #059669); color:white; padding:15px; border-radius:12px; text-align:center; font-weight:800;">Économise 10 000F</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- PAIEMENT ---
c1, c2 = st.columns([1.2, 0.8], gap="large")
with c1:
    st.markdown("""
    <div class="payment-box">
        <h3 style="margin-top:0;">💳 Paiement instantané - Activation en 5 min</h3>
        <p>Paye et envoie la capture sur WhatsApp, on active ton Dashboard direct.</p>
        <div style="display:flex; gap:20px; margin-top:15px;">
            <div style="background:white; padding:15px 20px; border-radius:12px; flex:1;">
                <b style="color:#ffcc00;">🟡 FLOOZ / MIXX</b><br>
                <span style="font-size:22px; font-weight:900;">97 04 42 09</span><br>
                <small>Nom: ENAM LANG</small>
            </div>
            <div style="background:white; padding:15px 20px; border-radius:12px; flex:1;">
                <b style="color:#0055ff;">🔵 T-MONEY</b><br>
                <span style="font-size:22px; font-weight:900;">91 29 63 08</span><br>
                <small>Nom: ENAM</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("### ⚡ Pourquoi 5000F c'est rien ?")
    st.write("Un seul téléphone oublié en stock = 15000F perdu. Ton Dashboard t'évite ça chaque semaine.")
    st.success("**ROI garanti:** Tu gagnes +50 000F de bénéfice en mieux gérant ton stock dès le 1er mois ou remboursé.")
    st.link_button("📲 ENVOYER PREUVE SUR WHATSAPP - ACTIVATION 5MIN", "https://wa.me/22897044209?text=Salut%20Enam%20!%20J'ai%20paye%20mon%20abonnement%20ENAM%20PHONE%20PRO%20voici%20la%20capture", use_container_width=True, type="primary")
    st.link_button("⬅️ Retour au tableau de bord", "/", use_container_width=True)

st.divider()
st.markdown("<center style='color:#999;'>🔒 Paiement 100% sécurisé via Flooz / TMoney | 📍 Lomé - Deckon - Togo | 💬 Support: +228 97 04 42 09</center>", unsafe_allow_html=True)
