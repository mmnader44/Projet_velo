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
        zoom=10,)
    fig.update_layout(
        mapbox_style="carto-positron", width=800, height=650, showlegend=False
    )

        # Afficher la figure dans Streamlit
    st.plotly_chart(fig)
with tab2:
    st.markdown(
    "<h2 style='color: black ; text-align: center;'>Services lié au Vélo</h2>",
    unsafe_allow_html=True,
    )
    df_count = df['Code postal'].value_counts().reset_index()
    df_count.columns = ['Code postal', 'Nombre']
    fig = px.bar(df_count, x='Code postal', y='Nombre', title='Nombre de valeurs par Code postal')

    # Afficher le graphique
    st.plotly_chart(fig)