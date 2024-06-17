# les imports
import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
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

# Fill NaN values with 0
df = df.fillna(0)

# Configuration initiale
st.set_page_config(
    page_title="Main page", layout="wide", initial_sidebar_state="expanded"
)

#________________Sidebar_______________
# Filtre dans la sidebar pour le type d'organisation et type de service
with st.sidebar:

    st.write("Quels services cherchez-vous ?")

    # Filtre associatif
    with st.expander("Type d'organisation :"):
        orga_list = ['Tous', 'Associatif', 'Entreprise']
        selected_orga_list = st.radio('Sélectionnez votre modèle :', orga_list)

    # Sélection du type de service
    with st.expander("Type de services"):
        type_service_list = ["Tous", "Ventes", "Location", "Réparation"]
        selected_type_service = st.radio("Sélectionnez votre service :", type_service_list)

# Filtrage du dataframe en fonction des choix faits dans la sidebar
if selected_orga_list == "Tous" and selected_type_service == "Tous":

    df_final = df  # Aucun filtrage appliqué

elif selected_orga_list == "Tous":
    # Filtrage uniquement par type de service
    if selected_type_service == "Ventes":
        df_final = df[df['Ventes'] == True]
    elif selected_type_service == "Location":
        df_final = df[df['Location'] == True]
    elif selected_type_service == "Réparation":
        df_final = df[df['Réparation'] == True]

elif selected_orga_list == "Associatif":

    # Filtrage par type d'organisation et éventuellement par type de service
    df_final = df[df['Type entreprise'] == 'Association']

    if selected_type_service != "Tous":
        if selected_type_service == "Ventes":
            df_final = df_final[df_final['Ventes'] == True]
        elif selected_type_service == "Location":
            df_final = df_final[df_final['Location'] == True]
        elif selected_type_service == "Réparation":
            df_final = df_final[df_final['Réparation'] == True]

elif selected_orga_list == "Entreprise":

    # Filtrage par type d'organisation "Entreprise" et éventuellement par type de service
    df_final = df[df['Type entreprise'] == 'Entreprise']

    if selected_type_service != "Tous":
        if selected_type_service == "Ventes":
            df_final = df_final[df_final['Ventes'] == True]
        elif selected_type_service == "Location":
            df_final = df_final[df_final['Location'] == True]
        elif selected_type_service == "Réparation":
            df_final = df_final[df_final['Réparation'] == True]
else:
    st.error('Sélection incorrecte')


#______________________Carte_____________________

st.markdown(
"<h1 style='color: black ; text-align: center;'>Nantes Bike Map : Localisation des Services Vélo</h1>",
unsafe_allow_html=True,
)

# Onglets
tab1, tab2 = st.tabs(
    ["CARTE", "DATAVIZ"]
)
with tab1:

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
            "latitude": False,
            "longitude": False,
            "Site Web": df_final['Site internet'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>'),
        },
        zoom=10,
        ).update_traces(marker={"size": 10})
    fig.update_layout(
        mapbox_style="carto-positron", width=1000, height=650, showlegend=False
    )

        # Afficher la figure dans Streamlit
    st.plotly_chart(fig)

with tab2:

    col1, col2 = st.columns(2)

    with col1:
        # Sommes pour Mécanique
        somme_mecanique = df_final[['Vente de vélos neufs Classique Mécanique', 
                            'Vente de vélos neufs Pliant Mécanique', 
                            'Vente de vélos neufs Cargo Mécanique', 
                            'Location Classique Mécanique',
                            'Location Pliant Mécanique', 
                            'Location Cargo Mécanique']].sum().sum()

        # Sommes pour Électrique (VAE/AE)
        somme_vae = df_final[['Vente de vélos neufs Classique VAE', 
                        'Vente de vélos neufs Pliant AE', 
                        'Vente de vélos neufs Cargo AE', 
                        'Location Classique VAE', 
                        'Location Pliant AE', 
                        'Location Cargo AE']].sum().sum()

        # Création du diagramme camembert 1
        labels = ['Mécanique', 'Électrique (AE)']
        sizes = [somme_mecanique, somme_vae]

        plt.figure(figsize=(2, 2))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=250)
        plt.title('      Electrique vs Mécanique      ')
        plt.legend(fontsize='xx-small', markerscale=0.1, loc='upper left')
        st.pyplot(plt.gcf())

    with col2:

        # Création du diagramme camembert 2
        labels = ['Associatif', 'Non-Associatif']
        sizes = [
            df_final[df_final['Type entreprise'] == 'Association'].shape[0],  # Nombre d'organismes associatifs
            df_final[df_final['Type entreprise'] == 'Entreprise'].shape[0]  # Nombre d'organismes non-associatifs
        ]

        plt.figure(figsize=(2, 2))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors = ['green','red'], startangle=150)
        plt.title("          Type d'organisme         ")
        plt.legend(fontsize='xx-small', markerscale=0.1, loc='upper left')
        st.pyplot(plt.gcf())
