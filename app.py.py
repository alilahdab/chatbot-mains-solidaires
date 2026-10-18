import streamlit as st
import google.generativeai as genai

# 1. Configuration de l'IA (Remplace par ta clé API Gemini)
# Tu peux en obtenir une gratuitement sur Google AI Studio
genai.configure(api_key="TA_CLE_API_ICI")
model = genai.GenerativeModel('gemini-pro')

# 2. Interface Graphique (GUI)
st.title("🎓 Chatbot du Club Les mains solidaires ")
st.write("Bienvenue ! Pose tes questions sur le club, les événements ou les inscriptions.")

# 3. Gestion de l'historique de conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher les anciens messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Zone de saisie pour l'étudiant
if user_input := st.chat_input("Écris ton message ici..."):
    # Afficher la question de l'utilisateur
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # On donne des consignes à l'IA pour qu'elle sache qu'elle représente le club
    prompt_context = f"Tu es le chatbot officiel et très sympa d'un club universitaire. Réponds de manière courte et dynamique à cette question d'un étudiant : {user_input}"

    # Demander la réponse à l'IA
    response = model.generate_content(prompt_context)

    # Afficher la réponse
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})