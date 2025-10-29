# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import os


SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

service_account_info = json.loads(st.secrets["general"]["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPE)
client = gspread.authorize(creds)



df = pd.read_csv("https://raw.githubusercontent.com/clemence-g/Politicaltest/3ae7e697af8cadd3cb1847ff6e5112d24ce6769c/votes.csv",sep=";", encoding="latin1")

photos_partis = {'DR' : "https://raw.githubusercontent.com/clemence-g/Politicaltest/c8a160c73198089e20e885e9bf189e85acbb45b6/Pictures/DR.jpg",
                'EPR':"https://raw.githubusercontent.com/clemence-g/Politicaltest/c8a160c73198089e20e885e9bf189e85acbb45b6/Pictures/EPR.jpg",
                'GDR' : "https://raw.githubusercontent.com/clemence-g/Politicaltest/c8a160c73198089e20e885e9bf189e85acbb45b6/Pictures/gdr.jpg",
                'HOR':"https://raw.githubusercontent.com/clemence-g/Politicaltest/c8a160c73198089e20e885e9bf189e85acbb45b6/Pictures/hor.jpeg",
                'LFI':"https://raw.githubusercontent.com/clemence-g/Politicaltest/c8a160c73198089e20e885e9bf189e85acbb45b6/Pictures/lfi.jpg",
                'DEM':"https://raw.githubusercontent.com/clemence-g/Politicaltest/c8a160c73198089e20e885e9bf189e85acbb45b6/Pictures/DEM.jpg",
                'LIOT':"https://raw.githubusercontent.com/clemence-g/Politicaltest/c8a160c73198089e20e885e9bf189e85acbb45b6/Pictures/liot.jpg",
                'RN':"https://raw.githubusercontent.com/clemence-g/Politicaltest/c8a160c73198089e20e885e9bf189e85acbb45b6/Pictures/RN.jpg", 
                'SOC':"https://raw.githubusercontent.com/clemence-g/Politicaltest/c8a160c73198089e20e885e9bf189e85acbb45b6/Pictures/SOC.jpg",
                'UDDPLR':"https://raw.githubusercontent.com/clemence-g/Politicaltest/c8a160c73198089e20e885e9bf189e85acbb45b6/Pictures/UDDPLR.jpg",
               'ECOS':"https://raw.githubusercontent.com/clemence-g/Politicaltest/c8a160c73198089e20e885e9bf189e85acbb45b6/Pictures/ECOS.jpg"}

acronyme_nom = {'DR' : "Droite Républicaine",
                'EPR':"Ensemble pour la République",
                'GDR' : "Gauche Démocrate et Républicaine",
                'HOR':"Horizons & Indépendants",
                'LFI':"La France insoumise - NFP",
                'DEM':"Les Démocrates",
                'LIOT':"Libertés, Indépendants, Outre-mer et Territoires",
                'RN':"Rassemblement National", 
                'SOC':"Socialistes et apparentés",
                'UDDPLR':"UDR",
               'ECOS':"Écologiste et Social"}
parti_liste = ['DR', 'EPR', 'GDR', 'HOR', 'LFI', 'DEM',
       'LIOT', 'RN', 'SOC', 'UDDPLR', 'ECOS']

colors = {
    "LFI": "#E94E77",
    "SOC": "#E6007E",
    "GDR": "#C00000",
    "ECOS": "#009E73",
    "DEM": "#FDB813",
    "HOR": "#4C9BE8",
    "EPR": "#FFD700",
    "DR": "#003366",
    "UDDPLR": "#1E64C8",
    "RN": "#1A237E",
    "LIOT": "#C7A76C"
}
#-------------------------------------------------------------------------------------------------------------------------


# --- Initialisation des points dans session_state pour garder l'état ---
if "points" not in st.session_state:
    st.session_state.points = {parti: 0 for parti in parti_liste}
if "vote_index" not in st.session_state:
    st.session_state.vote_index = 0
    
if 'historique' not in st.session_state:
    st.session_state.historique = []

if 'nom_utilisateur' not in st.session_state:
    st.session_state.nom_utilisateur = ""
    
    
def trouve_parti(vote, choix):   
    parti_ok = []
    
    for parti in parti_liste:
        if df.loc[vote,parti] == choix:
            parti_ok.append(parti)
            
    return parti_ok

def add_points(liste):
    for parti in liste:
        st.session_state.points[parti] += 1
def delete_points(liste):
    for parti in liste:
        st.session_state.points[parti] -= 1    

    
# --- Titre de l'application ---
st.title("Quiz Politique - À quel parti appartenez-vous ?")



if st.session_state.nom_utilisateur == "":
  nom_input = st.text_input("Nom/Pseudo :")

  if st.button("Commencer") and nom_input.strip() != "":
        st.session_state.nom_utilisateur = nom_input.strip()
        st.rerun()
  elif st.button("Commencer"):
        st.warning("Merci d'entrer un nom avant de commencer !")

  st.stop()  # ⛔ Stop ici tant que le nom n'est pas donné
st.stop()  
# --- Vérifier si on a fini tous les votes ---
if st.session_state.vote_index < len(df):
    vote = st.session_state.vote_index
    st.write("#### Vote", vote+1, "sur", len(df)+1)
    st.subheader(df.loc[vote, 'Titre'])
    
    
    pour = st.button("Pour", key=f"p_{vote}")
    contre = st.button("Contre", key=f"c_{vote}")
    abstention = st.button("Abstention", key=f"a_{vote}")
    choix = None
    
    if pour:
        choix = "P"
    elif contre:
        choix = "C"
    elif abstention:
        choix="A"
    

    if choix:
        liste_1 = trouve_parti(vote, choix)
        add_points(liste_1)
        
        st.session_state.historique.append({
        "vote": vote,
        "choix": choix,
        "partis": liste_1
      })

        st.session_state.vote_index += 1
        st.rerun()  # relance la page pour passer au vote suivant
       
    if st.session_state.vote_index >=1:
        if st.button("Back",type = "tertiary"):
            last_list = st.session_state.historique.pop()
            last_list = last_list["partis"]
            delete_points(last_list)

            st.session_state.vote_index -= 1
            st.rerun()

else:
    maximum = max(st.session_state.points.values())
    winners = []
    
    for k,v in st.session_state.points.items():
        if v == maximum:
          winners.append(k)
    if len(winners) == 1:
      gagnants_str = ", ".join(winners)
      sheet = client.open_by_key("1SzLS8_dZn-ET_Rwqc9hlm0xpkXWOuZMapKvehTrcN7g").sheet1
      sheet.append_row([nom_utilisateur, gagnants_str, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
      st.write("Le parti qui vous correspond le plus est", acronyme_nom[winners[0]], "(", winners[0], ")")
      st.write(f"[Voir la description du groupe sur datan.fr](https://datan.fr/groupes/legislature-17/{winners[0]})")
      col1, col2, col3 = st.columns([1,2,1])  # la colonne du milieu est plus large
      with col2:
          st.image(photos_partis[winners[0]]) 
    else:
      gagnants_str = ", ".join(winners)
      sheet = client.open_by_key("1SzLS8_dZn-ET_Rwqc9hlm0xpkXWOuZMapKvehTrcN7g").sheet1
      sheet.append_row([nom_utilisateur, gagnants_str, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        
      st.write("Les partis qui vous correspondent le plus sont: ")

      for parti in winners  :
          st.write(acronyme_nom[parti], "(",parti,")")
          st.write(f"[Voir la description du groupe sur datan.fr](https://datan.fr/groupes/legislature-17/{parti})")
          col1, col2, col3 = st.columns([1,2,1])  # la colonne du milieu est plus large
          with col2:
              st.image(photos_partis[parti]) 
          
    points_sorted = dict(sorted(st.session_state.points.items(), key=lambda item: int(item[1]), reverse=True))
   
    st.bar_chart(data=points_sorted, horizontal = True, x_label = "Points", y_label = "Partis", sort = False, use_container_width=False,width = 600,height = 400,color = "#ffaa00")

        
    
    recommencer = st.button("Recommencer le quiz", type = "primary")
    if recommencer :
        
        st.session_state.points = {parti: 0 for parti in parti_liste}
        st.session_state.vote_index = 0


        



















