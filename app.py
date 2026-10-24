import os
import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Assistant", page_icon="🤖", layout="centered"
)

# Custom CSS for clean ChatGPT-like look
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff;
        color: #333333;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar for Settings
with st.sidebar:
  st.title("⚙️ Control Panel")
  st.write("Powered by Groq AI Models")

  # Model Selection
  selected_model = st.selectbox(
      "Select AI Model",
      ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
  )

  # Clear Chat Button
  if st.button("🗑️ Clear Conversation"):
    st.session_state.messages = []
    st.rerun()

  st.markdown("---")
  st.markdown("🌐 **Multilingual Ready:** Type in any language!")
  st.markdown("🚀 **Hosted on Streamlit & GitHub**")

# Main Header
st.markdown(
    "<h1 style='text-align: center; color: #202123;'>AI Assistant</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #6e6e80;'>How can I help you"
    " today?</p>",
    unsafe_allow_html=True,
)

# API Key validation
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
  st.warning(
      "⚠️ Please set your `GROQ_API_KEY` in Streamlit secrets or environment"
      " variables."
  )
else:
  client = Groq(api_key=api_key)

  # Initialize chat history
  if "messages" not in st.session_state:
    st.session_state.messages = []

  # Display past messages
  for message in st.session_state.messages:
    # System message skip karein UI par dikhane ke liye
    if message["role"] != "system":
      with st.chat_message(message["role"]):
        st.markdown(message["content"])

  # User Input
  if prompt := st.chat_input("Message AI Assistant..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
      message_placeholder = st.empty()
      full_response = ""

      try:
        # System prompt to handle multiple languages dynamically
        system_prompt = {
            "role": "system",
            "content": (
                "You are a helpful AI assistant. Detect the language of the"
                " user's message and respond in that exact same language."
            ),
        }

        # Prepare messages including system instruction
        messages_payload = [system_prompt] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        completion = client.chat.completions.create(
            model=selected_model, messages=messages_payload, stream=True
        )

        for chunk in completion:
          if chunk.choices[0].delta.content:
            full_response += chunk.choices[0].delta.content
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

      except Exception as e:
        st.error(f"An error occurred: {e}")
