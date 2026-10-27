import streamlit as st
from google import genai

# 1. Récupération de toutes les clés disponibles
keys = []
for key_name in ["GEMINI_KEY_1", "GEMINI_KEY_2", "GEMINI_KEY_3", "GEMINI_API_KEY"]:
    if key_name in st.secrets and st.secrets[key_name]:
        keys.append(st.secrets[key_name])

# Clé de secours par défaut si aucun secret n'est trouvé
if not keys:
    keys = ["AQ.Ab8RN6KxA1KDv-RoHuop7_dWpPFg29R411iAW58uMZmdFpk6Hg"]

# 2. Interface Graphique
st.title("🎓 Chatbot du Club Les mains solidaires")
st.write("Bienvenue ! Posez vos questions sur le club, les événements ou les inscriptions.")

with st.sidebar:
    st.header("⚙️ Options")
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()

infos_club = """
Informations sur le club :
- Nom : Les mains solidaires
- Mission : Organisation caritative pour aider les étudiants et la communauté locale.
- Inscriptions : Elles sont ouvertes ! Il faut envoyer un mail à inscription@mainssolidaires.ma
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


# 3. Fonction d'envoi avec rotation automatique des clés et des modèles
def generate_response_with_fallback(prompt):
    models_to_try = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-1.5-flash"]

    for current_key in keys:
        client = genai.Client(api_key=current_key)
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                return response.text
            except Exception:
                continue  # Essaie le modèle/clé suivant en cas de quota dépassé

    return "⚠️ Tous les quotas gratuits temporaires sont épuisés. Merci de réessayer dans quelques minutes !"


# 4. Traitement du message
if user_input := st.chat_input("Écris ton message ici..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    prompt_context = f"Tu es le chatbot officiel du club 'Les mains solidaires'. Voici les informations : {infos_club}. Réponds de manière courte et sympathique à : {user_input}. IMPORTANT : Si tu mentionnes l'adresse email d'inscription, affiche-la sous forme de lien cliquable [inscription@mainssolidaires.ma](mailto:inscription@mainssolidaires.ma)."

    reply = generate_response_with_fallback(prompt_context)

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
