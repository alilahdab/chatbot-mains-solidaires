import streamlit as st
from google import genai


client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🎓 Chatbot du Club Les mains solidaires")
st.write("Bienvenue ! Posez vos questions sur le club, les événements ou les inscriptions.")


with st.sidebar:
    st.header("⚙️ Options")
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()


NOUVELLE_EMAIL = "mainssolidaires.inscription@gmail.com"

infos_club = f"""
Informations sur le club :
- Nom : Les mains solidaires
- Mission : Organisation caritative pour aider les étudiants et la communauté locale.
- Inscriptions : Elles sont ouvertes ! Il faut envoyer un mail à mainssolidaires.inscription@gmail.com 
- Président : Alae Zirari
- Vice président : Zahra Kaddour
- HR Manager : Nada Hammad
- Evenements manager : Ali Lahdab
- Media team : Douae Rais & Hidaya Zouhini
- Communication manager : Youssef El Aouni
- Treasurer : Nada El Ouardi
- General secretariat : Benryahi Nouhaida
"""


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if user_input := st.chat_input("Écris ton message ici..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    prompt_context = f"Tu es le chatbot officiel du club 'Les mains solidaires'. Voici les informations : {infos_club}. Réponds de manière courte et sympathique à : {user_input}. IMPORTANT : Si tu mentionnes l'adresse email d'inscription ({NOUVELLE_EMAIL}), affiche-la toujours comme un vrai lien cliquable (ex: [{NOUVELLE_EMAIL}](mailto:{NOUVELLE_EMAIL}))."

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt_context,
    )

    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
