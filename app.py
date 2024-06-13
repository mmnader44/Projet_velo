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
        orga_list = ['Tous', 'Associatif']
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
    df_final = df[df['Association'] == True]
    
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
"<h2 style='color: black ; text-align: center;'>Nantes Bike Map : Localisation des Services Vélo</h2>",
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
            "Site internet": True,
            "latitude": False,
            "longitude": False,
        },
        zoom=10,
        ).update_traces(marker={"size": 10})
    fig.update_layout(
        mapbox_style="carto-positron", width=1000, height=650, showlegend=False
    )

        # Afficher la figure dans Streamlit
    st.plotly_chart(fig)

with tab2:

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

    # Création du diagramme camembert 1
    labels = ['Mécanique', 'Électrique (AE)']
    sizes = [somme_mecanique, somme_vae]

    plt.figure(figsize=(4, 4))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=250)
    plt.axis('equal')  # Assurez-vous que le diagramme est un cercle
    plt.title('Répartition des services entre les vélos électrique et mécanique')  # Titre du diagramme
    plt.legend()  # Légende basée sur les labels
    st.pyplot(plt.gcf())

    # Création du diagramme camembert pour la répartition des types d'organismes
    labels = ['Associatif', 'Non-Associatif']
    sizes = [
        df[df['Association'] == True].shape[0],  # Nombre d'organismes associatifs
        df[df['Association'] == null].shape[0]  # Nombre d'organismes non-associatifs
    ]

    plt.figure(figsize=(4, 4))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=250)
    plt.axis('equal')  # Assurez-vous que le diagramme est un cercle
    plt.title("Répartition Types d'organismes")  # Titre du diagramme
    plt.legend()  # Légende basée sur les labels

    st.pyplot(plt.gcf())