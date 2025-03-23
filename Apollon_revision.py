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
        "IMAGE_QUESTION": pd.Series(dtype='str'),  # Nouvelle colonne pour l'image de la question
        "IMAGE_REPONSE": pd.Series(dtype='str'),  # Nouvelle colonne pour l'image de la réponse
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

def none_image(df):
  pixel_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
  df['IMAGE_QUESTION'] = df['IMAGE_QUESTION'].apply(lambda x: pixel_image_base64 if x == '' else x)
  df['IMAGE_REPONSE'] = df['IMAGE_REPONSE'].apply(lambda x: pixel_image_base64 if x == '' else x)
  return df


def download_csv(df, filename="flashcards.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Convertir en base64
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Télécharger le CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

none_image(st.session_state.df)

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
                        none_image(st.session_state.df)
                        st.success("Flashcards chargées avec succès !")
                    else:
                        st.error("Le fichier CSV doit contenir les colonnes 'INTITULE_QUESTION' et 'REPONSE_JUSTE'.")

            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier CSV : {e}")

    with st.expander("Créer des flashcards"):

        st.header("Créer des flashcards")
        question = st.text_input("Question :")
        image_question = st.file_uploader("Image pour la question (facultatif)", type=["jpg", "png", "jpeg"])

        reponse = st.text_input("Réponse :")
        image_reponse = st.file_uploader("Image pour la réponse (facultatif)", type=["jpg", "png", "jpeg"])

        if st.button("Ajouter Flashcard"):
            new_row = {
                    "INTITULE_QUESTION": question,
                    "REPONSE_JUSTE": reponse,
                    "IMAGE_QUESTION": base64.b64encode(image_question.read()).decode() if image_question else "",
                    "IMAGE_REPONSE": base64.b64encode(image_reponse.read()).decode() if image_reponse else "",
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
            new_row_df = pd.DataFrame([new_row])
            # Ajouter la nouvelle ligne au DataFrame existant
            st.session_state.df = pd.concat([st.session_state.df, new_row_df], ignore_index=True)
            none_image(st.session_state.df)

            st.success("Flashcard ajoutée avec succès !")
    with st.expander("Afficher le DataFrame"):  # Afficher dans un expander pour gagner de la place
        st.dataframe(st.session_state.df) 

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
                width: 600px;
                height: 400px;
                perspective: 1000px;
            }}
            .flip-card-front p, .flip-card-back p {{
                font-size: 24px;
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
                background-color: #e8e6e7;
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
        current_image_question = st.session_state.df.iloc[st.session_state.current_flashcard_index]["IMAGE_QUESTION"]
        current_image_reponse = st.session_state.df.iloc[st.session_state.current_flashcard_index]["IMAGE_REPONSE"]

        # HTML pour la flashcard
        html = f"""
        <div class="flip-card">
          <div class="flip-card-inner">
            <div class="flip-card-front">
              <p>{current_question}</p>
              {f"<img src='data:image/jpeg;base64,{current_image_question}' style='max-width: 100%; max-height: 100%;' />" if current_image_question else ""}
            </div>
            <div class="flip-card-back">
              <p>{current_answer}</p>
              {f"<img src='data:image/jpeg;base64,{current_image_reponse}' style='max-width: 100%; max-height: 100%;' />" if current_image_reponse else ""}
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

if page == "QCM":
    if st.session_state.df.empty:
        st.warning("Aucune flashcard créée pour le moment.")
        st.stop()  # Arrêter l'exécution si aucune flashcard

    if "qcm_current_index" not in st.session_state:
        st.session_state.qcm_current_index = 0

    # Obtenir la question et les réponses
    question = st.session_state.df.iloc[st.session_state.qcm_current_index]["INTITULE_QUESTION"]
    correct_answer = st.session_state.df.iloc[st.session_state.qcm_current_index]["REPONSE_JUSTE"]
    incorrect_answers = [
        st.session_state.df.iloc[st.session_state.qcm_current_index][col]
        for col in ["REPONSE_FAUSSE_1", "REPONSE_FAUSSE_2", "REPONSE_FAUSSE_3"]
        if st.session_state.df.iloc[st.session_state.qcm_current_index][col] != ""  # Ignorer les réponses fausses vides
    ]

    # Mélanger les réponses
    all_answers = [correct_answer] + incorrect_answers
    random.shuffle(all_answers)

    # Styles CSS pour les carrés
    st.markdown(
        """
        <style>
        .question-square {
            background-color: #f0f0f5;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 3px 3px 5px #888888;
        }
        .answer-button {
            background-color: #e0e0e5;
            border: none;
            padding: 15px 20px;
            border-radius: 5px;
            margin: 10px;
            width: 100%;
            text-align: center;
            cursor: pointer;
            box-shadow: 2px 2px 3px #888888;
            transition: background-color 0.3s ease;
        }
        .answer-button:hover {
            background-color: #d0d0d5;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    # Afficher la question
    st.markdown(f"<div class='question-square'>{question}</div>", unsafe_allow_html=True)

    # Afficher les réponses avec des clés uniques en utilisant hash()
    # Afficher les réponses comme des carrés cliquables
    cols = st.columns(2)
    for i, answer in enumerate(all_answers):
        with cols[i % 2]:
            key = hash(f"{question}_{answer}")  # Générer une clé unique avec hash()
            if st.button(answer, key=key):
                # Styles additionnels après clic
                key = hash(f"{question}_{answer}")
            
            # Utiliser st.markdown pour créer des carrés cliquables
            if st.markdown(f"<div class='answer-square' id='{key}' onclick='handleClick(this)' data-answer='{answer}'>{answer}</div>", unsafe_allow_html=True):
                if answer == correct_answer:
                    st.markdown(f"<div class='answer-button' style='background-color: #90ee90;'>{answer}</div>", unsafe_allow_html=True) # Vert pour la bonne réponse
                else:
                    st.markdown(f"<div class='answer-button' style='background-color: #ffcccb;'>{answer}</div>", unsafe_allow_html=True) # Rouge pour la mauvaise réponse
            else: 
                # Affichage initial du bouton
                st.markdown(f"<div class='answer-button'>{answer}</div>", unsafe_allow_html=True)
    # Bouton pour passer à la question suivante
    if st.button("Question suivante"):
        st.session_state.qcm_current_index = (st.session_state.qcm_current_index + 1) % len(st.session_state.df)
