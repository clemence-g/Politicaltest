# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 18:10:40 2025

@author: User
"""
import streamlit as st
import pandas as pd

df = pd.read_csv("https://github.com/clemence-g/Politicaltest/blob/b246cfea279cf604d7bd5ccef4fd5ed9e952d70d/votes.csv",sep=";", encoding="latin1")

acronyme_nom = {'DR' : "Droite Républicaine", 'EPR':"Ensemble pour la République", 'GDR' : "Gauche Démocrate et Républicaine", 'HOR':"Horizons & Indépendants", 'LFI':"La France insoumise - NFP", 'DEM':"Les Démocrates",
       'LIOT':"Libertés, Indépendants, Outre-mer et Territoires", 'RN':"Rassemblement National", 'SOC':"Socialistes et apparentés", 'UDDPLR':"UDR", 'ECOS':"Écologiste et Social"}
parti_liste = ['DR', 'EPR', 'GDR', 'HOR', 'LFI', 'DEM',
       'LIOT', 'RN', 'SOC', 'UDDPLR', 'ECOS']
points = {'DR':0, 'EPR':0, 'GDR':0, 'HOR':0, 'LFI':0, 'DEM':0,
       'LIOT':0, 'RN':0, 'SOC':0, 'UDDPLR':0, 'ECOS':0}
df.loc[1,'DR']



# --- Initialisation des points dans session_state pour garder l'état ---
if "points" not in st.session_state:
    st.session_state.points = {parti: 0 for parti in parti_liste}
if "vote_index" not in st.session_state:
    st.session_state.vote_index = 0
    
    
    
def trouve_parti(vote, choix):   
    parti_ok = []
    
    for parti in parti_liste:
        if df.loc[vote,parti] == choix:
            parti_ok.append(parti)
            
    return parti_ok

def add_points(liste):
    for parti in liste:
        st.session_state.points[parti] += 1
    

    
# --- Titre de l'application ---
st.title("Quiz Politique - À quel parti appartenez-vous ?")





# --- Vérifier si on a fini tous les votes ---
if st.session_state.vote_index < len(df):
    vote = st.session_state.vote_index
    st.write("### Vote", vote+1)
    st.write(df.loc[vote, 'Titre'])
    
    
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
        st.session_state.vote_index += 1
        st.rerun()  # relance la page pour passer au vote suivant

else:
    maximum = max(st.session_state.points.values())
    winners = []
    for k,v in st.session_state.points.items():
        if v == maximum:
            winners.append(k)
    if len(winners) == 1:
        st.write("Le parti qui vous correspond le plus est", acronyme_nom[winners[0]], "(", winners[0], ")")
        st.write(f"[Voir la description du groupe sur datan.fr](https://datan.fr/groupes/legislature-17/{winners[0]})")
    else:
        st.write("Les partis qui vous correspondent le plus sont: ")
        for parti in winners  :
            st.write(acronyme_nom[parti], "(",parti,")")
            st.write(f"[Voir la description du groupe sur datan.fr](https://datan.fr/groupes/legislature-17/{parti})")
    
    recommencer = st.button("Recommencer le quiz", type = "primary")
    if recommencer :
        
        st.session_state.points = {parti: 0 for parti in parti_liste}
        st.session_state.vote_index = 0


        
