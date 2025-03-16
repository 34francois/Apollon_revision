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
        "NBR_JUSTE" pd.Series(dtype='int'),
        "NBR_FAUX" pd.Series(dtype='int'),
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

# Initialisation des états de session
if "flashcards" not in st.session_state:
    st.session_state.flashcards = {}
if "flashcard_stats" not in st.session_state:
    st.session_state.flashcard_stats = {}
if "quizzes" not in st.session_state:
    st.session_state.quizzes = {}
if "current_card" not in st.session_state:
    st.session_state.current_card = ""


with st.sidebar:

    # Rubrique pour créer des flashcards
    st.header("Créer des flashcards")
    with st.form("new_card"):
        question = st.text_input("Question :")
        answer = st.text_input("Réponse :")
        if st.form_submit_button("Ajouter"):
            # Ajouter une nouvelle ligne à st.session_state.df
            new_row = pd.DataFrame({"INTITULE_QUESTION": [question], "REPONSE_JUSTE": [answer]})
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.success("Flashcard ajoutée !")


if page == "Chronologie":
    st.header("Chronologie")

    # Charger les dates depuis un fichier CSV ou une autre source de données
    dates_df = pd.DataFrame(
        [
            {"date": "2023-10-26", "événement": "Événement 1"},
            {"date": "2023-11-15", "événement": "Événement 2"},
            {"date": "2023-12-03", "événement": "Événement 3"},
        ]
    )

    # Trier les dates par ordre chronologique
    dates_df = dates_df.sort_values(by=["date"])

    # Afficher la chronologie sous forme de liste
    for index, row in dates_df.iterrows():
        st.markdown(f"**{row['date']}**: {row['événement']}")
    # Convertir les dates en format JSON pour JavaScript
    dates_json = dates_df.to_json(orient="records")

    # Afficher le composant chronologie en utilisant JavaScript
    st.components.v1.html(
        f"""
        <div id="timeline">
            <div class="fixed-square" style="left: 50px; top: 200px;"></div>
            <div class="fixed-square" style="left: 200px; top: 200px;"></div>
            <div class="fixed-square" style="left: 350px; top: 200px;"></div>
            <div class="fixed-square" style="left: 500px; top: 200px;"></div>
        </div>
        <script>
        const datesData = {dates_json};

        // Créer les carrés pour chaque date
        const timelineContainer = document.getElementById('timeline');
        datesData.forEach(date => {{
            const square = document.createElement('div');
            square.style.width = '100px';
            square.style.height = '100px';
            square.style.backgroundColor = 'lightblue';
            square.style.border = '1px solid black';
            square.style.margin = '10px';
            square.style.display = 'inline-block';
            square.style.position = 'absolute';
            square.textContent = date.date + ': ' + date.événement;
            timelineContainer.appendChild(square);

            // ... (Gestion du déplacement - modifiée)
            let isDragging = false;
            let offsetX, offsetY;

            square.addEventListener('mousedown', (e) => {{
                isDragging = true;
                offsetX = e.clientX - square.offsetLeft;
                offsetY = e.clientY - square.offsetTop;
            }});

            document.addEventListener('mouseup', () => {{
                isDragging = false;

                // Vérifier le chevauchement avec les carrés fixes
                const fixedSquares = document.querySelectorAll('.fixed-square');
                fixedSquares.forEach(fixedSquare => {{
                    if (isOverlapping(square, fixedSquare)) {{
                        // Centrer le carré sur le carré fixe
                        square.style.left = (fixedSquare.offsetLeft + (fixedSquare.offsetWidth - square.offsetWidth) / 2) + 'px';
                        square.style.top = (fixedSquare.offsetTop + (fixedSquare.offsetHeight - square.offsetHeight) / 2) + 'px';

                        // Changer la couleur du carré
                        square.style.backgroundColor = 'lightgreen'; 
                    }} else {{
                        // Remettre la couleur d'origine si pas de chevauchement
                        square.style.backgroundColor = 'lightblue';
                    }}
                }});
            }});

            document.addEventListener('mousemove', (e) => {{
                if (isDragging) {{
                    square.style.left = (e.clientX - offsetX) + 'px';
                    square.style.top = (e.clientY - offsetY) + 'px';
                }}
            }});
        }});

        // Styliser les carrés fixes
                const fixedSquares = document.querySelectorAll('.fixed-square');
                fixedSquares.forEach(square => {{
                    square.style.width = '50px';
                    square.style.height = '50px';
                    square.style.backgroundColor = 'gray';
                    square.style.border = '1px solid black';
                    square.style.position = 'absolute'; // Important pour le positionnement
                }});


        // Fonction pour vérifier le chevauchement entre deux éléments
        function isOverlapping(element1, element2) {{
            const rect1 = element1.getBoundingClientRect();
            const rect2 = element2.getBoundingClientRect();

            return !(
                rect1.right < rect2.left ||
                rect1.left > rect2.right ||
                rect1.bottom < rect2.top ||
                rect1.top > rect2.bottom
            );
        }}
        </script>
        """,
        height=800,
    )



if page == "Flashcards":
    # Sélectionner une flashcard aléatoire
    if not st.session_state.df.empty:
        random_index = random.randint(0, len(st.session_state.df) - 1)
        current_card = st.session_state.df.loc[random_index, "INTITULE_QUESTION"]
    else:
        current_card = ""  # Gérer le cas où df est vide
    
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
            background-color: #70b9c4;
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
    
    # Afficher les boutons "Juste" et "Faux"
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Juste"):
            if st.session_state.current_card in st.session_state.flashcard_stats:
                st.session_state.flashcard_stats[st.session_state.current_card]["correct"] += 1
            else:
                st.session_state.flashcard_stats[st.session_state.current_card] = {"correct": 1, "incorrect": 0}
            st.session_state.current_card = random.choice(list(st.session_state.flashcards.keys()))  # Passer à la carte suivante
    with col2:
        if st.button("Faux"):
            if st.session_state.current_card in st.session_state.flashcard_stats:
                st.session_state.flashcard_stats[st.session_state.current_card]["incorrect"] += 1
            else:
                st.session_state.flashcard_stats[st.session_state.current_card] = {"correct": 0, "incorrect": 1}
            st.session_state.current_card = random.choice(list(st.session_state.flashcards.keys()))  # Passer à la carte suivante
    # Afficher le bouton « Carte suivante »
    if st.button("Carte suivante"):
        st.session_state.current_card = random.choice(list(st.session_state.flashcards.keys()))
    # Bouton pour mettre à jour les statistiques dans st.session_state.flashcards
    if st.button("Mettre à jour les statistiques"):
        # Convertir les flashcards en DataFrame
        flashcards_df = pd.DataFrame(list(st.session_state.flashcards.items()), columns=["question", "answer"])

        # Ajouter les colonnes "juste" et "faux"
        flashcards_df["juste"] = flashcards_df["question"].apply(lambda question: st.session_state.flashcard_stats.get(question, {}).get("correct", 0))
        flashcards_df["faux"] = flashcards_df["question"].apply(lambda question: st.session_state.flashcard_stats.get(question, {}).get("incorrect", 0))

        # Mettre à jour st.session_state.flashcards avec les nouvelles données
        for index, row in flashcards_df.iterrows():
            question = row["question"]
            answer = row["answer"]
            correct = row["juste"]
            incorrect = row["faux"]

            if question in st.session_state.flashcards:  # Vérifier si la flashcard existe déjà
                st.session_state.flashcards[question] = {
                    "answer": answer,
                    "correct": correct,
                    "incorrect": incorrect
                }
            else:  # Ajouter la flashcard si elle n'existe pas
                st.session_state.flashcards[question] = {
                    "answer": answer,
                    "correct": correct,
                    "incorrect": incorrect
                }

        st.success("Statistiques mises à jour dans st.session_state.flashcards !")
    # Afficher les statistiques des flashcards (si disponibles)
    if st.session_state.flashcard_stats:
        st.header("Statistiques des flashcards")
        for question, stats in st.session_state.flashcard_stats.items():
            st.write(f"**Question :** {question}")
            st.write(f"Juste : {stats['correct']}, Faux : {stats['incorrect']}")
            st.write("---")

if page == "QCM":
    st.header("QCM")

    html_string = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    #quiz-container {
        width: 500px;
        margin: 0 auto;
        text-align: center;
    }

    #question {
        font-size: 20px;
        margin-bottom: 20px;
    }

    .choice {
        width: 500px;
        height: 100px;
        background-color: lightblue;
        border: 1px solid black;
        margin: 10px auto;
        display: block;
        cursor: pointer;
        line-height: 100px; /* Centre le texte verticalement */
        text-align: center;
        font-size: 18px;
    }

    .choice.selected {
        background-color: lightgreen;
    }

    #result {
        font-size: 18px;
        margin-top: 20px;
    }
    </style>
    </head>
    <body>
    <div id="quiz-container">
      <div id="question"></div>
      <div id="choices">
        <div class="choice" data-choice="A">A</div>
        <div class="choice" data-choice="B">B</div>
        <div class="choice" data-choice="C">C</div>
        <div class="choice" data-choice="D">D</div>
      </div>
      <div id="result"></div>
    </div>

    <script>
    const quizContainer = document.getElementById('quiz-container');
    const questionElement = document.getElementById('question');
    const choicesElement = document.getElementById('choices');
    const resultElement = document.getElementById('result');

    const questions = [
      {
        question: "Quelle est la capitale de la France ?",
        choices: ["Paris", "Londres", "Berlin", "Madrid"],
        answer: "A"
      },
      {
        question: "Quel est le plus grand océan du monde ?",
        choices: ["Océan Atlantique", "Océan Indien", "Océan Pacifique", "Océan Arctique"],
        answer: "C"
      },
      // Ajoutez d'autres questions ici
    ];

    let currentQuestion = 0;
    let selectedChoice = null; 

    function loadQuestion() {
      const question = questions[currentQuestion];
      questionElement.textContent = question.question;

      const choices = question.choices;
      for (let i = 0; i < choices.length; i++) {
        const choiceElement = choicesElement.children[i];
        choiceElement.textContent = choices[i];

        choiceElement.onclick = () => {
            // Désélectionner le choix précédent
            if (selectedChoice) {
                selectedChoice.classList.remove('selected');
            }
            // Sélectionner le nouveau choix
            selectedChoice = choiceElement; 
            selectedChoice.classList.add('selected');

            checkAnswer(choices[i]);
        };
      }
    }

    function checkAnswer(choice) {
      const question = questions[currentQuestion];
      if (choice === question.choices[question.answer.charCodeAt(0) - 'A'.charCodeAt(0)]) {
        resultElement.textContent = "Correct !";
      } else {
        resultElement.textContent = "Incorrect.";
      }

      // Passe à la question suivante après un délai
      setTimeout(() => {
        currentQuestion++;
        if (currentQuestion < questions.length) {
            selectedChoice = null; // Réinitialiser la sélection
            resultElement.textContent = ''; // Effacer le résultat précédent
            loadQuestion();
        } else {
            resultElement.textContent = "Fin du QCM.";
        }
      }, 1000); // Délai de 1 seconde (1000 millisecondes)
    }

    loadQuestion();
    </script>
    </body>
    </html>
    """

    st.components.v1.html(html_string, height=500)  # Ajuste la hauteur si nécessaire
