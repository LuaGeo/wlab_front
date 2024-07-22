import streamlit as st
import pandas as pd
import requests
import io

st.markdown(
    """
    <style>
    .main {
        background-color: #fff;
    }
    .stApp {
        color: #2a9390;
    }
    .stButton>button {
        background-color: #3cd1ce;
        color: white;
    }
    .stButton>button:hover {
        background-color: #2a9390;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Prédiction Cancer du Sein")
st.write("Veuillez charger les résultats des examens (.csv - 30 mesures nécessaires).")

uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")
def get_prediction(features):
    url = 'http://127.0.0.1:8000/api/predict/'
    response = requests.post(url, json={'features': features})
    return response.json()

if uploaded_file is not None:
    # Lire le fichier CSV
    df = pd.read_csv(uploaded_file, sep=';')

    # Afficher les colonnes pour debug
    st.write(f"Colonnes lues: {df.columns.tolist()}")
    st.write(f"Nombre de colonnes: {df.shape[1]}")
    
    if df.shape[1] != 30:
        st.error("Le fichier CSV doit contenir exactement 30 colonnes.")
    else:
        # Afficher le contenu du fichier
        st.write("Contenu du fichier chargé:")
        st.dataframe(df)

        # Faire la prédiction
        features = df.values.tolist()[0]
        prediction = get_prediction(features)
        
        st.write(f"Prédiction: {'Maligne' if prediction['prediction'] == 1 else 'Bénigne'}")

