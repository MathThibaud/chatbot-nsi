import streamlit as st
import random

# Charger les questions depuis le fichier
with open("questions.txt", "r", encoding="utf-8") as f:
    questions = [q.strip() for q in f if q.strip()]

st.set_page_config(page_title="Chatbot NSI – Révisions BAC")

st.title("🎓 Chatbot NSI – Révisions BAC Pratique")

# Mémoriser les questions/réponses
if "question_index" not in st.session_state:
    st.session_state.question_index = random.randint(0, len(questions) - 1)

if "responses" not in st.session_state:
    st.session_state.responses = []

# Afficher la question actuelle
current_question = questions[st.session_state.question_index]
st.markdown(f"**Question :** {current_question}")

# Zone de réponse multi-ligne
response = st.text_area("Ta réponse (code ou explication) :", height=200)

# Bouton pour envoyer la réponse
if st.button("✅ Envoyer"):
    if response.strip():
        st.session_state.responses.append((current_question, response))
        # Passer à une autre question au hasard
        st.session_state.question_index = random.randint(0, len(questions) - 1)
        st.experimental_rerun()

# Affichage des réponses précédentes
if st.session_state.responses:
    st.markdown("---")
    st.markdown("### 📚 Réponses précédentes :")
    for q, r in reversed(st.session_state.responses):
        st.markdown(f"**Q :** {q}")
        st.markdown("**Réponse :**")
        st.code(r, language="python")
