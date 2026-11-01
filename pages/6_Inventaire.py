# pages/Inventaire.py - EPPRO avec gestion PIN + INVENTAIRE AUTOMATIQUE
import streamlit as st
import pandas as pd
import json
import os
from datetime import date, datetime
import hashlib
st.set_page_config(page_title="Inventaire", page_icon="📦", layout="wide")

INVENTAIRE_FILE = "inventaire_historique.json"
STOCK_XLSX = "stock.xlsx"
CONFIG_FILE = "shop_config.json"
IMAGE_MAP = "images_map.json"
DEFAULT_PIN = "1234"

def get_pin_hash():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            return cfg.get("owner_pin_hash", hashlib.sha256(DEFAULT_PIN.encode()).hexdigest())
        except:
            pass
    return hashlib.sha256(DEFAULT_PIN.encode()).hexdigest()

def set_pin_hash(new_pin):
    cfg = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except:
            cfg = {}
    cfg["owner_pin_hash"] = hashlib.sha256(new_pin.encode()).hexdigest()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

def load_stock():
    if os.path.exists(STOCK_XLSX):
        try:
            df = pd.read_excel(STOCK_XLSX, dtype={"IMEI": str})
            return df
        except:
            pass
    if "df" in st.session_state:
        return st.session_state["df"]
    return pd.DataFrame()

def load_images():
    if os.path.exists(IMAGE_MAP):
        try:
            with open(IMAGE_MAP, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_historique(entry):
    hist = []
    if os.path.exists(INVENTAIRE_FILE):
        try:
            with open(INVENTAIRE_FILE, "r", encoding="utf-8") as f:
                hist = json.load(f)
        except:
            hist = []
    hist.append(entry)
    with open(INVENTAIRE_FILE, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=2, ensure_ascii=False)

PIN_HASH = get_pin_hash()
st.title("📦 Inventaire - Automatique")
st.caption(f"Comptage du {date.today().strftime('%d/%m/%Y')} - Version Auto")

tab_inventaire, tab_auto, tab_histo, tab_params = st.tabs(["📋 Comptage Manuel", "🤖 Auto Inventaire", "📜 Historique", "⚙️ PIN"])

with tab_inventaire:
    # --- TON ANCIEN CODE 100% GARDE ---
    df_stock = load_stock()
    if df_stock.empty:
        st.error("Aucun stock trouvé")
        st.stop()
    df_stock["IMEI"] = df_stock["IMEI"].astype(str)
    if "Marque" not in df_stock.columns: df_stock["Marque"]="Autre"
    if "Modèle" not in df_stock.columns: df_stock["Modèle"]=df_stock.iloc[:,1] if len(df_stock.columns)>1 else "Inconnu"
    if "Prix Achat (FCFA)" not in df_stock.columns: df_stock["Prix Achat (FCFA)"]=0
    if "📦 Statut" not in df_stock.columns: df_stock["📦 Statut"]="En Stock"
    df_theo = df_stock[df_stock["📦 Statut"]=="En Stock"].copy()
    st.info(f"Théorique : {len(df_theo)} téléphones | Valeur : {df_theo['Prix Achat (FCFA)'].sum():,} F")
    seuil_bas = st.slider("Seuil alerte stock bas par marque", 1, 10, 3, key="seuil_manuel")
    stock_par_marque = df_theo.groupby("Marque").size()
    marques_faibles = stock_par_marque[stock_par_marque <= seuil_bas]
    if not marques_faibles.empty:
        st.warning(f"⚠️ Stock faible : {', '.join([f'{m} ({q})' for m,q in marques_faibles.items()])}")
    st.subheader("1. Comptage physique")
    inventaire_rows = []
    for _, row in df_theo.iterrows():
        inventaire_rows.append({"IMEI": row["IMEI"], "Modèle": row["Modèle"], "Marque": row["Marque"], "Prix Achat": int(row["Prix Achat (FCFA)"]), "Théorique":1, "Réel":1, "État":"Bon", "Raison écart":""})
    df_edit = pd.DataFrame(inventaire_rows)
    edited = st.data_editor(df_edit, column_config={"IMEI": st.column_config.TextColumn(disabled=True), "Modèle": st.column_config.TextColumn(disabled=True), "Marque": st.column_config.TextColumn(disabled=True), "Prix Achat": st.column_config.NumberColumn(disabled=True, format="%d F"), "Théorique": st.column_config.NumberColumn(disabled=True), "Réel": st.column_config.SelectboxColumn(options=[0,1]), "État": st.column_config.SelectboxColumn(options=["Bon","Endommagé","Écran cassé","Incomplet","Volé","Perdu"], required=True), "Raison écart": st.column_config.TextColumn()}, hide_index=True, width='stretch', height=350)
    st.subheader("2. Validation et calcul")
    col1, col2 = st.columns(2)
    user_compte = col1.text_input("Qui a compté ? *", placeholder="ENAM", key="user_manuel")
    photo_preuve = col2.file_uploader("Photo preuve (optionnel)", type=["jpg","png"], key="photo_manuel")
    if st.button("Calculer écarts", type="primary", width='stretch', key="calc_manuel"):
        if not user_compte: st.error("Nom obligatoire")
        else:
            edited["Écart"] = edited["Réel"] - edited["Théorique"]
            manquants = edited[edited["Réel"]==0]
            endommages = edited[edited["État"]!="Bon"]
            perte_totale = manquants["Prix Achat"].sum() + endommages[~endommages.index.isin(manquants.index)]["Prix Achat"].sum()*0.5
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Manquants", f"{len(manquants)}"); c2.metric("Endommagés", f"{len(endommages)}"); c3.metric("Perte estimée", f"{perte_totale:,.0f} F"); c4.metric("Fiabilité", f"{(len(edited)-len(manquants))/len(edited)*100:.1f} %")
            if not manquants.empty: st.error("Manquants :"); st.dataframe(manquants[["IMEI","Modèle","Prix Achat","Raison écart"]], width='stretch')
            if not endommages.empty: st.warning("Endommagés :"); st.dataframe(endommages, width='stretch')
            st.session_state["last_edited"] = edited
            st.session_state["last_perte"] = perte_totale
    st.divider()
    if "last_edited" in st.session_state:
        st.subheader("3. Clôture inventaire")
        pin = st.text_input("PIN Propriétaire pour valider ajustement", type="password", key="pin_manuel")
        if st.button("Valider et ajuster stock", width='stretch', key="val_manuel"):
            if hashlib.sha256(pin.encode()).hexdigest() != PIN_HASH: st.error("PIN incorrect")
            else:
                edited_final = st.session_state["last_edited"]
                manquants = edited_final[edited_final["Réel"]==0]
                for _, r in manquants.iterrows():
                    idx = df_stock[df_stock["IMEI"]==r["IMEI"]].index
                    if len(idx)>0: df_stock.at[idx[0], "📦 Statut"] = r["État"]
                try:
                    df_stock.to_excel(STOCK_XLSX, index=False)
                    if "df" in st.session_state: st.session_state.df = df_stock
                except: pass
                save_historique({"date": str(date.today()), "heure": datetime.now().strftime("%H:%M:%S"), "par": user_compte, "manquants": len(manquants), "endommages": len(edited_final[edited_final["État"]!="Bon"]), "perte": int(st.session_state["last_perte"]), "details": edited_final.to_dict(orient="records"), "type": "MANUEL"})
                st.success("Inventaire validé et stock ajusté"); st.balloons()

with tab_auto:
    st.markdown("### 🤖 Inventaire 100% Automatique")
    st.caption("Le système compare automatiquement ton stock théorique avec la réalité")
    
    df_stock = load_stock()
    images = load_images()
    
    if df_stock.empty:
        st.error("Stock vide")
        st.stop()

    # AUTOMATIQUE 1 : Calcul instantané
    df_theo = df_stock[df_stock["📦 Statut"]=="En Stock"].copy() if "📦 Statut" in df_stock.columns else df_stock.copy()
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("📦 En Stock Théorique", len(df_theo))
    col_b.metric("💰 Valeur Théorique Achat", f"{df_theo['Prix Achat (FCFA)'].sum():,.0f} F" if "Prix Achat (FCFA)" in df_theo.columns else "0")
    col_c.metric("🖼️ Avec Photo Vitrine", f"{len([i for i in df_theo['IMEI'].astype(str) if str(i) in images])} / {len(df_theo)}")

    # AUTOMATIQUE 2 : Detection anomalies
    st.divider()
    st.subheader("🔍 Détection automatique d'anomalies")
    
    anomalies = []
    for _, row in df_theo.iterrows():
        imei = str(row["IMEI"])
        if imei not in images:
            anomalies.append({"IMEI": imei, "Modèle": row.get("Modèle",""), "Problème": "Pas de photo vitrine", "Gravité": "Faible"})
        if "Prix Achat (FCFA)" in row and "Prix de vente (FCFA)" in row:
            if row["Prix de vente (FCFA)"] <= row["Prix Achat (FCFA)"]:
                anomalies.append({"IMEI": imei, "Modèle": row.get("Modèle",""), "Problème": "Prix vente <= Prix achat (perte)", "Gravité": "CRITIQUE"})

    if anomalies:
        st.error(f"{len(anomalies)} anomalies détectées automatiquement")
        st.dataframe(pd.DataFrame(anomalies), width='stretch')
    else:
        st.success("✅ Aucune anomalie - Stock propre")

    # AUTOMATIQUE 3 : Alerte stock bas automatique
    st.subheader("📉 Alertes Stock Bas Automatiques")
    if not df_theo.empty:
        seuil_auto = st.slider("Seuil alerte auto", 1, 10, 3, key="seuil_auto")
        par_marque = df_theo.groupby("Marque").size().reset_index(name="Qté")
        par_marque["Alerte"] = par_marque["Qté"].apply(lambda x: "🔴 A COMMANDER" if x <= seuil_auto else "🟢 OK")
        st.dataframe(par_marque, width='stretch')
        
        a_commander = par_marque[par_marque["Qté"] <= seuil_auto]
        if not a_commander.empty:
            st.warning(f"Il faut recommander : {', '.join(a_commander['Marque'].tolist())}")

    # AUTOMATIQUE 4 : Inventaire en 1 clic
    st.divider()
    st.subheader("⚡ Inventaire Flash en 1 Clic")
    st.caption("Au lieu de cocher 0/1 à la main, clique ici pour dire que tout le stock théorique est bien là")
    
    col1, col2 = st.columns(2)
    user_auto = col1.text_input("Qui valide l'auto inventaire ?", placeholder="ENAM", key="user_auto")
    
    if st.button("🤖 LANCER INVENTAIRE AUTOMATIQUE", type="primary", width='stretch'):
        if not user_auto:
            st.error("Nom obligatoire")
        else:
            # Tout est considéré présent
            edited_auto = df_theo.copy()
            edited_auto["Réel"] = 1
            edited_auto["Écart"] = 0
            edited_auto["État"] = "Bon"
            
            save_historique({
                "date": str(date.today()),
                "heure": datetime.now().strftime("%H:%M:%S"),
                "par": user_auto,
                "manquants": 0,
                "endommages": 0,
                "perte": 0,
                "type": "AUTO",
                "details": [{"IMEI": str(r["IMEI"]), "Modèle": r.get("Modèle",""), "Statut": "OK Auto"} for _, r in edited_auto.iterrows()]
            })
            st.success(f"✅ Inventaire automatique validé par {user_auto} - {len(edited_auto)} téléphones comptés comme présents")
            st.balloons()
            st.metric("Fiabilité Auto", "100%")

with tab_histo:
    st.subheader("Historique")
    if os.path.exists(INVENTAIRE_FILE):
        try:
            with open(INVENTAIRE_FILE, "r", encoding="utf-8") as f:
                hist = json.load(f)
            if hist:
                st.dataframe(pd.DataFrame([{"Date":h["date"],"Heure":h.get("heure",""),"Par":h["par"],"Type":h.get("type","MANUEL"),"Manquants":h["manquants"],"Perte":h["perte"]} for h in hist[-30:]]), width='stretch')
            else: st.info("Aucun historique")
        except: st.info("Aucun historique")
    else: st.info("Aucun historique")

with tab_params:
    st.caption("🔒Zone propriétaire - PIN commun / Inventaire")
    st.subheader("⚙️ Modifier PIN Propriétaire")
    with st.form("change_pin"):
        old_pin = st.text_input("Ancien PIN *", type="password")
        new_pin = st.text_input("Nouveau PIN (4 chiffres) *", type="password")
        confirm_pin = st.text_input("Confirmer nouveau PIN *", type="password")
        submit = st.form_submit_button("Changer PIN", type="primary", width='stretch')
        if submit:
            if hashlib.sha256(old_pin.encode()).hexdigest() != PIN_HASH: st.error("Ancien PIN incorrect")
            elif len(new_pin) < 4: st.error("PIN trop court, min 4 chiffres")
            elif new_pin != confirm_pin: st.error("Confirmation différente")
            else:
                set_pin_hash(new_pin)
                st.success(f"✅ PIN changé avec succès ! Nouveau PIN : {new_pin}")
                st.balloons()
