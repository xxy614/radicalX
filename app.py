import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

# Project ID
project = "modular-shard-422903-b8"
vertexai.init(project=project)

# Configuration for the model
config = generative_models.GenerationConfig(
    temperature=0.4
)

# Load model with config
model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)
chat = model.start_chat()

# Helper function to display and send streamlit message
def llm_function(chat: ChatSession, query, initial=False):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    if not initial:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )
    
    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )

    with st.chat_message("model"):
        st.markdown(output)

st.title("Gemini Explorer")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# Add initial model message if it's a new session
if not st.session_state.initialized and len(st.session_state.messages) == 0:
    st.session_state.initialized = True  # Set this first to avoid race condition
    initial_prompt = "Introduce yourself as ReX, an kind assistant powered by Google Gemini. You use emojis to be interactive"
    response = chat.send_message(initial_prompt)  # Directly send the initial message to avoid recursive calls
    output = response.candidates[0].content.parts[0].text
    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )
    with st.chat_message("model"):
        st.markdown(output)

# Display and load chat history
for index, message in enumerate(st.session_state.messages):
    role = message["role"]
    content = message["content"]

    with st.chat_message(role):
        st.markdown(content)

# Capture user input
query = st.chat_input("Gemini Explorer")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)