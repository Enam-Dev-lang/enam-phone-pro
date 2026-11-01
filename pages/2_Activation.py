import streamlit as st, os, json, pandas as pd, random, string, platform, hashlib, uuid
from datetime import datetime, timedelta

def get_machine_id():
    raw = platform.node() + str(uuid.getnode())
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

LICENCE_FILE = "licence.json"
KEYS_FILE = "keys_database.json"
STOCK_FILE = "stock.xlsx"
CAISSE_FILE = "caisse_journal.json"
CODE_FILE = "manager_codes.json"
MASTER_KEYS = ["ENAM-MASTER-2026", "ENAM-ADMIN", "DEMO-2026"]

def is_activated():
    if not os.path.exists(LICENCE_FILE):
        return False, None
    try:
        with open(LICENCE_FILE, "r") as f:
            data = json.load(f)
        if not data.get("active", False):
            return False, None
        # Verrouillage PC
        if data.get("type") == "CLIENT" and "machine_id" in data:
            if data["machine_id"] != get_machine_id():
                return False, "MACHINE_DIFFERENTE"
        # ETAPE 4: Verif expiration
        if "expiry_date" in data and data["expiry_date"]:
            expiry = datetime.fromisoformat(data["expiry_date"])
            if datetime.now() > expiry:
                return False, f"EXPIRE_{data.get('plan','')}"
        return True, data
    except:
        return False, None

def load_keys():
    if not os.path.exists(KEYS_FILE):
        return {}
    try:
        with open(KEYS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_keys(data):
    with open(KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def FORCE_RESET():
    try:
        df_vide = pd.DataFrame(columns=["IMEI","Modèle","Marque","Prix Achat"])
        df_vide.to_excel(STOCK_FILE, index=False)
        with open(CAISSE_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    except:
        pass

# --- EN-TETE ---
st.markdown("""
<div style="background: linear-gradient(90deg, #0B6BD4, #0E7490); padding:20px; border-radius:12px">
<h1 style="margin:0; color:white; font-size:24px;">ENAM PHONE PRO</h1>
<p style="margin:0; color:#E0F2FE;">Centre d'Activation</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔑 1. Activation Licence", "👥 2. Codes Managers"])

with tab1:
    st.markdown("## 🔍 Activation de votre licence")
    
    active, info = is_activated()

    if active:
        plan = info.get('plan', 'MASTER')
        expiry = info.get('expiry_date', 'Illimité')
        if expiry != 'Illimité' and expiry:
            try:
                dt = datetime.fromisoformat(expiry)
                jours_restants = (dt - datetime.now()).days
                st.success(f"✅ Licence {plan} active - Expire le {dt.strftime('%d/%m/%Y')} ({jours_restants} jours restants)")
            except:
                st.success(f"✅ Licence {plan} active")
        else:
            st.success("✅ Licence MASTER active - Illimité")
        
        st.write(f"PC ID: `{get_machine_id()}`")
        if st.button("Se déconnecter / Changer de clé"):
            if os.path.exists(LICENCE_FILE):
                os.remove(LICENCE_FILE)
            st.rerun()
    else:
        # Gestion expiration
        if info and "EXPIRE" in str(info):
            st.error(f"⏰ Votre abonnement {info.replace('EXPIRE_','')} a expiré ! Repayez 5000F ou 50000F dans Abonnement pour recevoir une nouvelle clé.")
            st.link_button("💳 Aller payer", "pages/1_Abonnement.py")

        st.info("Entrez la clé reçue après paiement Mixx/Flooz")
        cle = st.text_input("Collez votre clé ici", placeholder="ENAM-XXXX-XXXX")
        
        if st.button("Activer maintenant", type="primary", use_container_width=True):
            cle_clean = cle.strip().upper()
            # 1. Clé MASTER
            if cle_clean in MASTER_KEYS:
                with open(LICENCE_FILE, "w") as f:
                    json.dump({"active": True, "key": cle_clean, "type": "MASTER", "plan": "MASTER", "machine_id": get_machine_id(), "activated_at": str(datetime.now()), "expiry_date": ""}, f)
                FORCE_RESET()
                st.success("✅ Clé MASTER activée (illimité)")
                st.balloons()
                st.rerun()
            # 2. Clé client avec expiration
            else:
                all_keys = load_keys()
                if cle_clean in all_keys:
                    if all_keys[cle_clean].get("used", False):
                        st.error("❌ Cette clé a déjà été utilisée.")
                    else:
                        plan = all_keys[cle_clean].get("plan", "MENSUEL")
                        duree = all_keys[cle_clean].get("duration_days", 30)
                        expiry_date = datetime.now() + timedelta(days=duree)

                        all_keys[cle_clean]["used"] = True
                        all_keys[cle_clean]["used_at"] = str(datetime.now())
                        all_keys[cle_clean]["machine_id"] = get_machine_id()
                        save_keys(all_keys)
                        
                        with open(LICENCE_FILE, "w") as f:
                            json.dump({"active": True, "key": cle_clean, "type": "CLIENT", "plan": plan, "machine_id": get_machine_id(), "activated_at": str(datetime.now()), "expiry_date": expiry_date.isoformat()}, f)
                        FORCE_RESET()
                        st.success(f"✅ Licence {plan} activée pour {duree} jours - Jusqu'au {expiry_date.strftime('%d/%m/%Y')}")
                        st.balloons()
                        st.rerun()
                else:
                    st.error("❌ Clé invalide.")

with tab2:
    active, _ = is_activated()
    if not active:
        st.error("🔒 Tu dois d'abord activer ta licence dans l'onglet 1")
        st.stop()
    st.markdown("### Générer un code pour chaque vendeur")
    codes = load_json(CODE_FILE, {})
    col1, col2 = st.columns([2,1])
    with col1:
        manager_name = st.text_input("Nom du vendeur", placeholder="Ex: Enam")
    with col2:
        st.write("")
        st.write("")
        if st.button("🔍 Générer", type="primary", use_container_width=True):
            if not manager_name.strip():
                st.error("Entre un nom")
            else:
                new_code = "MGR-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
                while new_code in codes:
                    new_code = "MGR-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
                codes[new_code] = {"manager": manager_name.strip(), "created": datetime.now().strftime("%d/%m/%Y %H:%M"), "uses": 0, "active": True}
                save_json(CODE_FILE, codes)
                st.success(f"Code pour {manager_name}")
                st.code(new_code)
    st.divider()
    if codes:
        for code, info in list(codes.items()):
            a,b,c,d = st.columns([2,2,1,1])
            with a: st.markdown(f"**{code}**")
            with b: st.write(f"{info['manager']} - {info['created']}")
            with c: st.write(f"{info['uses']} ventes")
            with d:
                if st.button("❌", key=f"del_{code}"):
                    del codes[code]
                    save_json(CODE_FILE, codes)
                    st.rerun()