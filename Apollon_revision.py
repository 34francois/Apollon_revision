import streamlit as st
import random
import pandas as pd

# Initialiser les flashcards (vide au départ)
if "flashcards" not in st.session_state:
    st.session_state.flashcards = {}
if "quizzes" not in st.session_state:
    st.session_state.quizzes = {}
# Créer les onglets
tabs = ["Flashcards", "QCM"]
selected_tab = st.sidebar.radio("Sélectionnez un onglet", tabs)

if selected_tab == "Flashcards":
    # Initialiser l'état de l'application
    if "current_card" not in st.session_state:
        st.session_state.current_card = ""  # Vide au départ
    
    # Rubrique pour créer des flashcards
    st.header("Créer des flashcards")
    with st.form("new_card"):
        question = st.text_input("Question :")
        answer = st.text_input("Réponse :")
        if st.form_submit_button("Ajouter"):
            st.session_state.flashcards[question] = answer
            st.success("Flashcard ajoutée !")
            
    # Charger les flashcards à partir d'un fichier CSV
    st.header("Charger des flashcards à partir d'un fichier CSV")
    uploaded_file = st.file_uploader("Choisir un fichier CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # Assurez-vous que le fichier CSV a des colonnes nommées "question" et "answer"
        for index, row in df.iterrows():
            st.session_state.flashcards[row["question"]] = row["answer"]
        st.success("Flashcards chargées à partir du fichier CSV !")
        
    # Sélectionner une flashcard aléatoire si les flashcards ne sont pas vides
    if st.session_state.flashcards:
        if not st.session_state.current_card:
            st.session_state.current_card = random.choice(list(st.session_state.flashcards.keys()))
    
    # Définir les styles CSS pour les flashcards
    st.markdown(
        """
        <style>
        .flip-card {
            background-color: transparent;
            width: 300px;
            height: 200px;
            perspective: 1000px;
        }
        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.8s;
            transform-style: preserve-3d;
        }
        .flip-card:hover .flip-card-inner {
            transform: rotateY(180deg);
        }
        .flip-card-front, .flip-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            border: 1px solid #ccc;
            padding: 20px;
            border-radius: 10px;
            background-color: #f7f7f7;
            box-shadow: 5px 5px 10px #888888;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .flip-card-front {
            color: black;
        }
        .flip-card-back {
            color: black;
            transform: rotateY(180deg); 
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Afficher la flashcard avec l'animation de retournement et la réponse au dos
    html = f"""
    <div class="flip-card">
      <div class="flip-card-inner">
        <div class="flip-card-front">
          <p>{st.session_state.current_card}</p>
        </div>
        <div class="flip-card-back">
          <p>{st.session_state.flashcards[st.session_state.current_card] if st.session_state.current_card in st.session_state.flashcards else ""}</p> 
        </div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    # Afficher la question
    st.markdown(f'<div class="card"><div class="question">{st.session_state.current_card}</div></div>', unsafe_allow_html=True)
    
    
    # Afficher le bouton « Carte suivante »
    if st.button("Carte suivante"):
        st.session_state.current_card = random.choice(list(st.session_state.flashcards.keys()))

elif selected_tab == "QCM":
    st.header("Créer un QCM")
    with st.form("new_quiz"):
        question = st.text_input("Question :")
        options = [st.text_input(f"Option {i+1} :") for i in range(4)]
        correct_answer = st.radio("Réponse correcte :", options)
        if st.form_submit_button("Ajouter"):
            st.session_state.quizzes[question] = {"options": options, "correct_answer": correct_answer}
            st.success("QCM ajouté !")

    # Afficher les QCM existants (si présents)
    if st.session_state.quizzes:
        st.header("QCM existants")
        for question, data in st.session_state.quizzes.items():
            st.write(f"**Question :** {question}")
            for option in data["options"]:
                st.write(f"- {option}")
            st.write(f"**Réponse correcte :** {data['correct_answer']}")
            st.write("---")
