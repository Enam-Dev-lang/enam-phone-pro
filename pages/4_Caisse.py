# pages/Caisse.py - Version PRO avec nom Caisse
import streamlit as st, json, os, hashlib
from datetime import datetime, date
import pandas as pd
import calendar

st.set_page_config(page_title="Caisse", page_icon="💰", layout="wide")

CAISSE_FILE = "caisse_journal.json"
CONFIG_FILE = "shop_config.json"
METHODS = ["Espèces", "Flooz", "TMoney", "Mixx"]
DEFAULT_PIN = "1234"
SEUIL_ALERTE = 50000

def get_pin_hash():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                return cfg.get("owner_pin_hash", hashlib.sha256(DEFAULT_PIN.encode()).hexdigest())
        except: pass
    return hashlib.sha256(DEFAULT_PIN.encode()).hexdigest()

def set_pin_hash(new_pin):
    cfg = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f: cfg = json.load(f)
        except: cfg = {}
    cfg["owner_pin_hash"] = hashlib.sha256(new_pin.encode()).hexdigest()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f: json.dump(cfg, f, indent=2, ensure_ascii=False)

def load_caisse():
    if not os.path.exists(CAISSE_FILE): return {}
    try:
        with open(CAISSE_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {}

def save_caisse(data):
    with open(CAISSE_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=2, ensure_ascii=False)

def log_action(action_type, details, user="Système"):
    with open("caisse_audit.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {user} | {action_type} | {details}\n")

def get_today_data(all_data, today_str):
    return all_data.get(today_str, {
        "ouverture": {m: 0 for m in METHODS}, "ventes_auto": {m: 0 for m in METHODS},
        "ventes_manuelles": [], "depenses": [], "transferts": [],
        "ouverture_par": "", "heure_ouverture": "", "cloture": False,
        "heure_cloture": "", "cloture_par": "", "comptage_reel": {}, "ecarts": {}, "logs": []
    })

def add_log(today_data, action, user, montant=0, methode="", note=""):
    today_data.setdefault("logs",[]).append({"heure": datetime.now().strftime("%H:%M:%S"),"user": user,"action": action,"montant": montant,"methode": methode,"note": note})
    log_action(action, f"{montant}F {methode} - {note}", user)

def calc_jour_stats(day_data):
    ouverture = sum(day_data.get("ouverture",{}).values())
    ventes_auto = sum(day_data.get("ventes_auto",{}).values())
    ventes_man = sum([v.get("montant",0) for v in day_data.get("ventes_manuelles",[])])
    depenses = sum([d.get("montant",0) for d in day_data.get("depenses",[])])
    ventes_tot = ventes_auto + ventes_man
    return {"ouverture":ouverture, "ventes_auto":ventes_auto, "ventes_man":ventes_man, "ventes_tot":ventes_tot, "depenses":depenses, "theorique":ouverture+ventes_tot-depenses, "benef":ventes_tot-depenses, "par_methode":{m:{"ouv":day_data.get("ouverture",{}).get(m,0),"v_auto":day_data.get("ventes_auto",{}).get(m,0),"v_man":sum([v["montant"] for v in day_data.get("ventes_manuelles",[]) if v.get("methode")==m]),"dep":sum([d["montant"] for d in day_data.get("depenses",[]) if d.get("methode")==m])} for m in METHODS}}

all_data = load_caisse()
today_str = str(date.today())
today_data = get_today_data(all_data, today_str)

soldes_theoriques = {}
for m in METHODS:
    soldes_theoriques[m] = today_data.get("ouverture",{}).get(m,0) + today_data.get("ventes_auto",{}).get(m,0) + sum([v["montant"] for v in today_data.get("ventes_manuelles",[]) if v.get("methode")==m]) - sum([d["montant"] for d in today_data.get("depenses",[]) if d.get("methode")==m]) + sum([t["montant"] if t.get("vers")==m else -t["montant"] for t in today_data.get("transferts",[])])

st.title("💰 Caisse")
st.caption(f"Journée du {date.today().strftime('%d/%m/%Y')}")

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Espèces", f"{soldes_theoriques['Espèces']:,} F"); c2.metric("Flooz", f"{soldes_theoriques['Flooz']:,} F"); c3.metric("TMoney", f"{soldes_theoriques['TMoney']:,} F"); c4.metric("Mixx", f"{soldes_theoriques['Mixx']:,} F"); c5.metric("TOTAL", f"{sum(soldes_theoriques.values()):,} F")
st.divider()

tabs = st.tabs(["Ouverture","Opérations","Transfert","Clôture","Contrôle","🔒","📊 Bilan"])

with tabs[0]:
    if today_data.get("ouverture_par"): st.success(f"Ouvert à {today_data.get('heure_ouverture')} par {today_data.get('ouverture_par')}"); st.json(today_data.get("ouverture"))
    else:
        with st.form("ouverture"):
            c1,c2 = st.columns(2); user_ouv = c1.text_input("Qui ouvre ? *")
            o_espece = c1.number_input("Espèces",0,step=1000); o_flooz = c2.number_input("Flooz",0,step=1000); o_tmoney = c1.number_input("TMoney",0,step=1000); o_mixx = c2.number_input("Mixx",0,step=1000)
            if st.form_submit_button("Valider Ouverture", width='stretch'):
                today_data["ouverture"]={"Espèces":o_espece,"Flooz":o_flooz,"TMoney":o_tmoney,"Mixx":o_mixx}; today_data["ouverture_par"]=user_ouv; today_data["heure_ouverture"]=datetime.now().strftime("%H:%M:%S")
                add_log(today_data,"OUVERTURE",user_ouv,sum([o_espece,o_flooz,o_tmoney,o_mixx]),"TOUS",""); all_data[today_str]=today_data; save_caisse(all_data); st.rerun()

with tabs[1]:
    col_a,col_b = st.columns(2)
    with col_a:
        st.markdown("**Sortie**")
        with st.form("depense"):
            user_dep=st.text_input("Qui sort ? *"); montant=st.number_input("Montant",100,step=500); methode=st.selectbox("Méthode",METHODS); motif=st.selectbox("Motif",["Retrait proprio","Achat stock","Crédit","Loyer","Transport","Autre"]); note=st.text_area("Justification *"); pin=st.text_input("PIN si >50k",type="password") if montant>=SEUIL_ALERTE else ""
            if st.form_submit_button("Enregistrer Dépense", type="primary"):
                if hashlib.sha256(pin.encode()).hexdigest()!=get_pin_hash() and montant>=SEUIL_ALERTE: st.error("PIN incorrect")
                else: today_data.setdefault("depenses",[]).append({"heure":datetime.now().strftime("%H:%M:%S"),"user":user_dep,"montant":montant,"methode":methode,"motif":motif,"note":note}); add_log(today_data,"DEPENSE",user_dep,montant,methode,f"{motif} - {note}"); all_data[today_str]=today_data; save_caisse(all_data); st.rerun()
    with col_b:
        st.markdown("**Vente manuelle**")
        with st.form("vente_man"):
            user_v=st.text_input("Vendeur *",key="user_v"); montant_v=st.number_input("Montant",100,step=1000,key="mont_v"); methode_v=st.selectbox("Méthode",METHODS,key="meth_v"); note_v=st.text_input("Produit / Raison")
            if st.form_submit_button("Ajouter Vente"): today_data.setdefault("ventes_manuelles",[]).append({"heure":datetime.now().strftime("%H:%M:%S"),"user":user_v,"montant":montant_v,"methode":methode_v,"note":note_v}); add_log(today_data,"VENTE_MANUELLE",user_v,montant_v,methode_v,note_v); all_data[today_str]=today_data; save_caisse(all_data); st.rerun()

with tabs[2]:
    with st.form("transfert"):
        user_t=st.text_input("Qui transfère ?"); de=st.selectbox("De",METHODS); vers=st.selectbox("Vers",[m for m in METHODS if m!=de]); mont_t=st.number_input("Montant",1000,step=1000)
        if st.form_submit_button("Transférer"): today_data.setdefault("transferts",[]).append({"heure":datetime.now().strftime("%H:%M:%S"),"user":user_t,"de":de,"vers":vers,"montant":mont_t}); add_log(today_data,"TRANSFERT",user_t,mont_t,f"{de}->{vers}",""); all_data[today_str]=today_data; save_caisse(all_data); st.success(f"{mont_t}F {de}->{vers}"); st.rerun()

with tabs[3]:
    if today_data.get("cloture"): st.success(f"Clôturé à {today_data.get('heure_cloture')} par {today_data.get('cloture_par')}"); st.json(today_data.get("ecarts"))
    else:
        with st.form("cloture_form"):
            user_clot=st.text_input("Qui clôture ? *"); c1,c2=st.columns(2); reel_espece=c1.number_input("Réel Espèces",0,step=500); reel_flooz=c2.number_input("Réel Flooz",0,step=500); reel_tmoney=c1.number_input("Réel TMoney",0,step=500); reel_mixx=c2.number_input("Réel Mixx",0,step=500); pin_clot=st.text_input("PIN Propriétaire",type="password")
            if st.form_submit_button("Clôturer", width='stretch'):
                if hashlib.sha256(pin_clot.encode()).hexdigest()!=get_pin_hash(): st.error("PIN incorrect")
                else:
                    comptage={"Espèces":reel_espece,"Flooz":reel_flooz,"TMoney":reel_tmoney,"Mixx":reel_mixx}; ecarts={m: comptage[m]-soldes_theoriques[m] for m in METHODS}
                    today_data["comptage_reel"]=comptage; today_data["ecarts"]=ecarts; today_data["cloture"]=True; today_data["heure_cloture"]=datetime.now().strftime("%H:%M:%S"); today_data["cloture_par"]=user_clot
                    add_log(today_data,"CLOTURE",user_clot,sum(comptage.values()),"TOUS",f"Ecarts:{ecarts}"); all_data[today_str]=today_data; save_caisse(all_data); st.balloons(); st.rerun()

with tabs[4]:
    pin_view=st.text_input("PIN Propriétaire",type="password",key="pin_view")
    if hashlib.sha256(pin_view.encode()).hexdigest()==get_pin_hash():
        st.success("Accès propriétaire"); 
        if today_data.get("logs"): st.dataframe(pd.DataFrame(today_data.get("logs")), width='stretch')

with tabs[5]:
    # TITRE CACHÉ - comme demandé
    st.caption("🔒 Zone propriétaire")
    with st.form("change_pin_caisse"):
        old_pin = st.text_input("Ancien PIN *", type="password", key="old_c")
        new_pin = st.text_input("Nouveau PIN *", type="password", key="new_c")
        confirm_pin = st.text_input("Confirmer *", type="password", key="conf_c")
        if st.form_submit_button("Changer PIN", type="primary", width='stretch'):
            if hashlib.sha256(old_pin.encode()).hexdigest() != get_pin_hash(): st.error("Ancien PIN incorrect")
            elif len(new_pin) < 4: st.error("PIN trop court")
            elif new_pin != confirm_pin: st.error("Confirmation différente")
            else: set_pin_hash(new_pin); st.success(f"✅ PIN changé : {new_pin}"); st.balloons()

with tabs[6]:
    pin_bilan = st.text_input("PIN pour Bilan", type="password", key="pin_bilan")
    if hashlib.sha256(pin_bilan.encode()).hexdigest() != get_pin_hash():
        st.warning("PIN requis pour Bilan"); st.stop()
    st.success("Accès Bilan")
    if not all_data: st.info("Pas d'historique"); st.stop()
    df_dates = []
    for d_str, d_data in all_data.items():
        try:
            dt = datetime.strptime(d_str, "%Y-%m-%d").date()
            stats = calc_jour_stats(d_data)
            df_dates.append({"date": dt, "date_str": d_str, "annee": dt.year, "mois": dt.month, **stats})
        except: continue
    df_bilan = pd.DataFrame(df_dates).sort_values("date")
    b1,b2,b3,b4 = st.tabs(["Journalier","Mensuel","Annuel","Prévisions"])
    with b1:
        date_sel = st.date_input("Choisir une date", value=date.today())
        date_sel_str = str(date_sel)
        if date_sel_str in all_data:
            stats = calc_jour_stats(all_data[date_sel_str])
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Ventes", f"{stats['ventes_tot']:,} F"); c2.metric("Dépenses", f"{stats['depenses']:,} F"); c3.metric("Bénéfice", f"{stats['benef']:,} F"); c4.metric("Théorique", f"{stats['theorique']:,} F")
            st.dataframe(pd.DataFrame(stats["par_methode"]).T, width='stretch')
            if all_data[date_sel_str].get("logs"): st.dataframe(pd.DataFrame(all_data[date_sel_str]["logs"]), width='stretch')
        else: st.warning(f"Aucune donnée pour {date_sel_str}")
        if not df_bilan.empty:
            st.markdown("**30 derniers jours**")
            st.line_chart(df_bilan.tail(30).set_index("date")[["ventes_tot","depenses","benef"]])
            st.dataframe(df_bilan.tail(30)[["date_str","ventes_tot","depenses","benef"]].sort_values("date", ascending=False), width='stretch')
    with b2:
        if not df_bilan.empty:
            mensuel = df_bilan.groupby(["annee","mois"]).agg(ventes_tot=("ventes_tot","sum"), depenses=("depenses","sum"), benef=("benef","sum"), jours=("date","count")).reset_index()
            mensuel["mois_label"] = mensuel.apply(lambda x: f"{x['annee']}-{x['mois']:02d}", axis=1)
            st.bar_chart(mensuel.set_index("mois_label")[["ventes_tot","depenses","benef"]])
            st.dataframe(mensuel.sort_values(["annee","mois"], ascending=False), width='stretch')
    with b3:
        if not df_bilan.empty:
            annuel = df_bilan.groupby("annee").agg(ventes_tot=("ventes_tot","sum"), depenses=("depenses","sum"), benef=("benef","sum"), jours=("date","count")).reset_index()
            st.bar_chart(annuel.set_index("annee")[["ventes_tot","depenses","benef"]]); st.dataframe(annuel, width='stretch')
    with b4:
        if len(df_bilan) >= 3:
            moy_7 = df_bilan.tail(7)["ventes_tot"].mean(); moy_30 = df_bilan.tail(30)["ventes_tot"].mean(); moy_benef_7 = df_bilan.tail(7)["benef"].mean()
            c1,c2,c3 = st.columns(3); c1.metric("Moy 7j CA", f"{moy_7:,.0f} F"); c2.metric("Moy 30j CA", f"{moy_30:,.0f} F"); c3.metric("Bénéf 7j", f"{moy_benef_7:,.0f} F")
            c1,c2,c3 = st.columns(3); c1.metric("Proj 7j", f"{moy_7*7:,.0f} F"); c2.metric("Proj 30j", f"{moy_30*30:,.0f} F"); c3.metric("Bénéf 30j", f"{moy_benef_7*30:,.0f} F")
            jours_restants = calendar.monthrange(date.today().year, date.today().month)[1] - date.today().day
            prev_fin_mois = df_bilan[df_bilan["mois"]==date.today().month]["ventes_tot"].sum() + moy_7 * jours_restants
            st.metric(f"Prévision fin {calendar.month_name[date.today().month]}", f"{prev_fin_mois:,.0f} F")
            try:
                import numpy as np
                x = np.array(range(len(df_bilan))); y = np.array(df_bilan["ventes_tot"])
                coeffs = np.polyfit(x, y, 1)
                tendance = "📈 Hausse" if coeffs[0] > 0 else "📉 Baisse" if coeffs[0] < 0 else "➡️ Stable"
                st.info(f"Tendance: {tendance} ({coeffs[0]:.2f} F/jour)")
            except: pass
