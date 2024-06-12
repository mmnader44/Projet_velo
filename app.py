# les imports
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# memoire session_state
if "df" not in st.session_state:
    chemin = Path(__file__).parent
    fichier_data = chemin / "Data" / "df_vélo_final.csv"
    df = pd.read_csv(fichier_data, sep=",")
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

# Configuration initiale
st.set_page_config(
    page_title="Main page", layout="wide", initial_sidebar_state="expanded"
)

#________________Sidebar_______________
with st.sidebar:
    st.write("Quels services cherchez-vous ?")
    
    # Sélection du type de service
    with st.expander("Type de services"):
        type_service_list = ["Tous", "Ventes", "Location", "Réparation"]
        selected_type_service = st.radio("Type de service :", type_service_list)

        # Filtrage du dataframe selon le type de service sélectionné
        if selected_type_service == "Tous":
            df_final = df
        elif selected_type_service == "Ventes":
            df_final = df[df['Ventes'] == True]
        elif selected_type_service == "Réparation":
            df_final = df[df['Réparation'] == True]
        elif selected_type_service == "Location":
            df_final = df[df['Location'] == True]

# Titrage
st.markdown(
    "<h2 style='color: black ; text-align: center;'>Services lié au vélo</h2>",
    unsafe_allow_html=True,
)
#______________________Carte_____________________

fig = px.scatter_mapbox(
    df_final,
    lat="latitude",
    lon="longitude",
    hover_name="Nom de l'enseigne",
    hover_data={
        "Adresse": True,
        "Ville": True,
        "Téléphone": True,
        "Mail": True,
        "Site internet": True,
        "latitude": False,
        "longitude": False,
    },
    zoom=10,)
    

fig.update_layout(
    mapbox_style="carto-positron", width=800, height=650, showlegend=False
    )

    # Afficher la figure dans Streamlit
st.plotly_chart(fig)

# # création d'un DF pour l'affichage
# columns_to_show = [
#     "Nom de l'établissement",
#     "Adresse de l'établissement",
#     "email",
#     "N° de téléphone",
#     "Site Web",
# ]
# available_columns = [col for col in columns_to_show if col in df_filtered.columns]
# df_show = df_filtered[available_columns]

# if selected_etab == "Pas de sélection":
#     st.write("Choisissez un  pour la recommandation")
# else:
#     st.write(
#         f"""Vous avez choisi {df_reco.iloc[0]["Nom de l'établissement"]}\n
#     L'adresse est le {df_reco.iloc[0]["Adresse de l'établissement"]}\n
#     L'adresse mail est le {df_reco.iloc[0]["email"]}\n
#     Joignable au {df_reco.iloc[0]["N° de téléphone"]}\n
#     Site internet {df_reco.iloc[0]["Site Web"]}\n
#     {df_reco.iloc[0]["information 1"]}\n
#     {df_reco.iloc[0]["information 2"]}\n
#     NaN signifie que la donnée n'a pas été entrée.\n
#     \n
#     \n
#     Rendez-vous sur la page hébergement pour voir les hébergements les plus proches.
#     """
#     )
