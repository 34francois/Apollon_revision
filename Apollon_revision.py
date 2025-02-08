import streamlit as st
import random

# Initialiser les flashcards (vide au départ)
if "flashcards" not in st.session_state:
    st.session_state.flashcards = {}

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
        background-color: #f0f0f0;
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
