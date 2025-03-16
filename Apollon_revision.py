import streamlit as st
import random
import pandas as pd
import base64
import streamlit.components.v1 as components
from streamlit_navigation_bar import st_navbar
import io

# Initialisation dans st.session_state
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "INTITULE_QUESTION": pd.Series(dtype='str'),
        "REPONSE_JUSTE": pd.Series(dtype='str'),
        "REPONSE_FAUSSE_1": pd.Series(dtype='str'),
        "REPONSE_FAUSSE_2": pd.Series(dtype='str'),
        "REPONSE_FAUSSE_3": pd.Series(dtype='str'),
        "REPONSE_FAUSSE_4": pd.Series(dtype='str'),
        "REPONSE_FAUSSE_5": pd.Series(dtype='str'),
        "REPONSE_FAUSSE_6": pd.Series(dtype='str'),
        "REPONSE_FAUSSE_7": pd.Series(dtype='str'),
        "REPONSE_FAUSSE_8": pd.Series(dtype='str'),
        "NBR_JUSTE" : pd.Series(dtype='int'),
        "NBR_FAUX" : pd.Series(dtype='int'),
    })
    

# Configuration de la barre de navigation
pages = ["Flashcards", "QCM", "Chronologie"]
styles = {
    "nav": {"background-color": "#9ea4f0", "justify-content": "left"},
    "img": {"padding-right": "14px"},
    "span": {"color": "white", "padding": "14px"},
    "active": {"background-color": "white", "color": "var(--text-color)", "font-weight": "normal", "padding": "14px"},
}
options = {"show_menu": False, "show_sidebar": False}
page = st_navbar(pages, styles=styles)

def download_csv(df, filename="flashcards.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Convertir en base64
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Télécharger le CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

with st.sidebar:
    with st.expander("Charger des flashcards d'un CSV"):
        # Ajout de la fonctionnalité de téléchargement de CSV
        uploaded_file = st.file_uploader("Charger un fichier CSV", type=["csv"])
        
        if uploaded_file is not None:
            try:
                # Charger le CSV dans un DataFrame
                new_flashcards = pd.read_csv(uploaded_file)
                
                # Afficher les questions dans un tableau
                st.subheader("Questions du fichier CSV:")
                st.dataframe(new_flashcards)
                
                # Bouton pour charger les données dans df
                
                if st.button("Charger les flashcards"):
                    # Vérifier si les colonnes nécessaires sont présentes
                    required_columns = ["INTITULE_QUESTION", "REPONSE_JUSTE"]
                    if all(col in new_flashcards.columns for col in required_columns):
                        # Concaténer le nouveau DataFrame avec le DataFrame existant
                        st.session_state.df = pd.concat([st.session_state.df, new_flashcards], ignore_index=True)
                        st.success("Flashcards chargées avec succès !")
                    else:
                        st.error("Le fichier CSV doit contenir les colonnes 'INTITULE_QUESTION' et 'REPONSE_JUSTE'.")
    
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier CSV : {e}")
        
    with st.expander("Créer des flashcards"):
    
        st.header("Créer des flashcards")
        question = st.text_input("Question :")
        reponse = st.text_input("Réponse :")
    
        if st.button("Ajouter Flashcard"):
                # Create a new row as a dictionary
                new_row = {
                    "INTITULE_QUESTION": question,
                    "REPONSE_JUSTE": reponse,
                    "REPONSE_FAUSSE_1": "",  # Add or modify other columns as needed
                    "REPONSE_FAUSSE_2": "",
                    "REPONSE_FAUSSE_3": "",
                    "REPONSE_FAUSSE_4": "",
                    "REPONSE_FAUSSE_5": "",
                    "REPONSE_FAUSSE_6": "",
                    "REPONSE_FAUSSE_7": "",
                    "REPONSE_FAUSSE_8": "",
                    "NBR_JUSTE": 0,
                    "NBR_FAUX": 0
                }
        
                # Append the new row to the DataFrame
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
    st.dataframe(st.session_state.df)
    st.subheader("Télécharger les flashcards:")
    download_csv(st.session_state.df)


if page == "Flashcards":
    if st.session_state.df.empty:
        st.warning("Aucune flashcard créée pour le moment.")
    else:
        if "current_flashcard_index" not in st.session_state:
            st.session_state.current_flashcard_index = 0

        # Définir les styles CSS pour les flashcards
        st.markdown(
            f"""
            <style>
            .flip-card {{
                background-color: transparent;
                width: 300px;
                height: 200px;
                perspective: 1000px;
            }}
            .flip-card-inner {{
                position: relative;
                width: 100%;
                height: 100%;
                text-align: center;
                transition: transform 0.8s;
                transform-style: preserve-3d;
            }}
            .flip-card:hover .flip-card-inner {{
                transform: rotateY(180deg);
            }}
            .flip-card-front, .flip-card-back {{
                position: absolute;
                width: 100%;
                height: 100%;
                -webkit-backface-visibility: hidden;
                backface-visibility: hidden;
                border: 1px solid #ccc;
                padding: 20px;
                border-radius: 10px;
                background-color: #c47094;
                box-shadow: 5px 5px 10px #888888;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .flip-card-front {{
                color: black;
            }}
            .flip-card-back {{
                color: black;
                transform: rotateY(180deg); 
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Afficher la flashcard courante
        current_question = st.session_state.df.iloc[
            st.session_state.current_flashcard_index
        ]["INTITULE_QUESTION"]
        current_answer = st.session_state.df.iloc[
            st.session_state.current_flashcard_index
        ]["REPONSE_JUSTE"]

        # HTML pour la flashcard
        html = f"""
        <div class="flip-card">
          <div class="flip-card-inner">
            <div class="flip-card-front">
              <p>{current_question}</p>
            </div>
            <div class="flip-card-back">
              <p>{current_answer}</p> 
            </div>
          </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    # Bouton pour afficher la flashcard suivante
    if st.button("Flashcard suivante"):
        st.session_state.current_flashcard_index = (
            st.session_state.current_flashcard_index + 1
        ) % len(st.session_state.df)  # Boucle à la première flashcard si on arrive à la fin
