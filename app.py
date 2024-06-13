# les imports
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go


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

#______________________Carte_____________________

# Onglets
tab1, tab2 = st.tabs(
    ["CARTE", "DATAVIZ"]
)
with tab1:
    st.markdown(
    "<h2 style='color: black ; text-align: center;'>Services lié au Vélo</h2>",
    unsafe_allow_html=True,
    )
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
        zoom=10,).update_traces(marker={"size": 10})
    fig.update_layout(
        mapbox_style="carto-positron", width=1000, height=650, showlegend=False
    )

        # Afficher la figure dans Streamlit
    st.plotly_chart(fig)

with tab2:
    st.markdown(
    "<h2 style='color: black ; text-align: center;'>Services lié au Vélo</h2>",
    unsafe_allow_html=True,
    )

    # Sommes pour Mécanique
    somme_mecanique = df[['Vente de vélos neufs Classique Mécanique', 
                        'Vente de vélos neufs Pliant Mécanique', 
                        'Vente de vélos neufs Cargo Mécanique', 
                        'Location Classique Mécanique',
                        'Location Pliant Mécanique', 
                        'Location Cargo Mécanique']].sum().sum()

    # Sommes pour Électrique (VAE/AE)
    somme_vae = df[['Vente de vélos neufs Classique VAE', 
                    'Vente de vélos neufs Pliant AE', 
                    'Vente de vélos neufs Cargo AE', 
                    'Location Classique VAE', 
                    'Location Pliant AE', 
                    'Location Cargo AE']].sum().sum()
    
    fig = go.Figure(data=[go.Table(
    header=dict(values=['Catégorie', 'Somme']),
    cells=dict(values=[['Mécanique', 'Électrique (AE)'],
                       [somme_mecanique, somme_vae]])
    )])

    fig.update_layout(title='Répartition des services entre les vélos éléctrique et mécanique')
    st.plotly_chart(fig)
