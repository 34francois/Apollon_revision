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



with st.sidebar:
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
    st.data_editor(st.session_state.df)
