import textwrap
import streamlit as st
from IPython.core.display import Markdown
import google.generativeai as genai
import config

config.local_css("style.css")
config.add_bg_from_url(config.background_link)

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

def to_markdown(text):
    text = text.replace('•', ' *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

if st.button("Back"):
    st.switch_page("pages/page4.py")
st.markdown("<h1 style='text-align: center; color: black;'>DoggoCare</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Chat with DoggoBot!</h1>", unsafe_allow_html=True)

genai.configure(api_key=config.GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Display chat messages from history
for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("Hi! I'm Doggo. Ask me anything about your dog"):
    # Display user's last message
    st.chat_message("user").markdown(prompt)

    details_dict = config.profiles_dict[config.current_profile]
    # Send user entry to Gemini and read the response
    edited_prompted = f"Answer this question: {prompt}, according to these details: " \
                      f"Dog's name: {config.current_profile}, " \
                      f"Breed: {details_dict['breed']}," \
                      f"Weight: {details_dict['weight']}, " \
                      f"Date of Birth: {details_dict['dob']}," \
                      f"Gender: {details_dict['gender']}, " \
                      f"Last haircut: {details_dict['last_haircut']},"\
                      f"Last hexagon vaccination: {details_dict['last_hexagon']}, " \
                      f"Last rabis vaccination: {details_dict['last_rabis']}, " \
                      f"Last spirocerca vaccination: {details_dict['last_spirocerca']}. " \
                      f"If you don't have enough details answer by general knowledge you have"
    response = st.session_state.chat.send_message(edited_prompted, safety_settings=safety_settings)

    with st.chat_message("assistant"):
        st.markdown(response.text)
