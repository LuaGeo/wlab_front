import streamlit as st
import pandas as pd
import requests
from streamlit_navigation_bar import st_navbar

st.set_page_config(initial_sidebar_state="collapsed")

pages = ["Diabètes", "Cancer du sein", "Maladie rénale chronique", "Maladie chronique cardiaque", "Maladie du foie"]

image_url = "/Users/lua/wild/project3/wlab_front/img/logo_wlab4 (1).svg"

themes = {
    "Standard": {
        "background-color": "#3cd1ce",
        "font-color": "#fff",
        "hover-color": "#2a9390",
        "active-color": "rgba(255, 255, 255, 0.25)"
    },
    "Daltonien": {
        "background-color": "#ffb3b3",  # Rouge doux
        "font-color": "#000000",  # Noir
        "hover-color": "#cc0000",  # Rouge foncé
        "active-color": "rgba(0, 0, 0, 0.25)"  # Noir transparent
    }
}

# Place the theme selectbox in the upper-right corner
theme_choice = st.selectbox(
    "Choisissez un thème de couleur :", 
    ["Standard", "Daltonien"], 
    key="theme_selectbox", 
    help="Choisissez un thème de couleur adapté."
)

selected_theme = themes[theme_choice]

styles = {
    "nav": {
        "background-color": selected_theme["background-color"],
        "font-size": "18px",
        "display": "flex",
        "justify-content": "center",
        "height": "200px",
        "width": "100vw",
        "padding": "none !important",
    },
    "img": {
        "url": f"{image_url}",
        "height": "150px",
        "margin-left": "-250px",
        "color": selected_theme["font-color"],
    },
    "div": {
        "text-decoration": "none",
        "padding": "10px",
        "font-weight": "bold",
        "max-width": "60rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": selected_theme["font-color"],
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {
        "background-color": selected_theme["active-color"],
        "color": selected_theme["hover-color"],
    },
    "hover": {
        "color": selected_theme["hover-color"],
    }
}


menu = st_navbar(pages, styles=styles, logo_path=image_url)
# st.write(menu)
st.markdown(
    f"""
    <style>
    .main {{
        background-color: #fff;
    }}
    .st-emotion-cache-1629p8f h1 {{
        color: {selected_theme["hover-color"]};
    }}
    .stApp {{
        color: {selected_theme["hover-color"]};
    }}
    .stButton>button {{
        background-color: {selected_theme["background-color"]};
        color: {selected_theme["font-color"]};
    }}
    .stButton>button:hover {{
        background-color: {selected_theme["hover-color"]};
        color: {selected_theme["font-color"]};
    }}
    .st-emotion-cache-h7cybc {{
        background-color: rgb(60, 209, 206, 0.15);
        border: 1px solid {selected_theme["hover-color"]};
    }}
    .st-emotion-cache-6rlrad {{
        color: {selected_theme["hover-color"]};
    }}
    /* Additional styles to make selectbox more discreet */
    .stSelectbox {{
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: {selected_theme["background-color"]};
        color: {selected_theme["font-color"]};
        border: 1px solid {selected_theme["hover-color"]};
        border-radius: 5px;
        padding: 5px;
        z-index: 1000;  /* Ensure it stays on top */
    }}
    .stSelectbox select {{
        background-color: {selected_theme["background-color"]};
        color: {selected_theme["font-color"]};
        border: none;
        outline: none;
        padding: 5px;
        border-radius: 5px;
    }}
    footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        color: {selected_theme["hover-color"]};
        padding: 10px;
        text-align: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Diagnostic")

# Fonction pour faire la prédiction
def get_prediction(features, disease_url):
    response = requests.post(disease_url, json={'features': features})
    st.write(f"Code de statut HTTP: {response.status_code}")
    st.write(f"Contenu brut de la réponse: {response.content}")
    if response.status_code != 200:
        st.error("La requête a échoué avec le code de statut HTTP: " + str(response.status_code))
        return None
    try:
        return response.json()
    except ValueError:
        st.error("La réponse n'est pas un JSON valide.")
        return None

def predict_disease(disease_name, disease_url):
    uploaded_file = st.file_uploader(f"Choisissez un fichier CSV pour {disease_name}", type="csv")

    if uploaded_file is not None:
        # Lire le fichier CSV
        df = pd.read_csv(uploaded_file, sep=",")

        # Afficher les colonnes pour déboguer
        st.write(f"Colonnes lues: {df.columns.tolist()}")
        st.write(f"Nombre de colonnes: {df.shape[1]}")

        st.write("Contenu du fichier chargé:")
        st.dataframe(df)

        # Faire la prédiction
        features = df.values.tolist()[0]
        prediction = get_prediction(features, disease_url)

        if prediction:
            st.write(f"Prédiction: {prediction['prediction']}")


# Définir les URL des API pour chaque maladie
disease_urls = {
    "Diabètes": 'http://127.0.0.1:8000/api/predict/diabetes/',
    "Cancer du sein": 'http://127.0.0.1:8000/api/predict/cancer/',
    "Maladie rénale chronique": 'http://127.0.0.1:8000/api/predict/renal/',
    "Maladie chronique cardiaque": 'http://127.0.0.1:8000/api/predict/cardiac/',
    "Maladie du foie": 'http://127.0.0.1:8000/api/predict/foie/',
}

# Afficher la section correspondante en fonction de l'onglet sélectionné
if menu == "Diabètes":
    predict_disease("Diabètes", disease_urls["Diabètes"])
elif menu == "Cancer du sein":
    predict_disease("Cancer du sein", disease_urls["Cancer du sein"])
elif menu == "Maladie rénale chronique":
    predict_disease("Maladie rénale chronique", disease_urls["Maladie rénale chronique"])
elif menu == "Maladie chronique cardiaque":
    predict_disease("Maladie chronique cardiaque", disease_urls["Maladie chronique cardiaque"])
elif menu == "Maladie du foie":
    predict_disease("Maladie du foie", disease_urls["Maladie du foie"])


st.markdown(
    """
    <footer>
        <p>Développé par <span style="font-weight:bold;">Wild's Anatomy ©</span></p>
    </footer>
    """,
    unsafe_allow_html=True
)