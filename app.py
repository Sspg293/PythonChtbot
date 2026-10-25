import streamlit as st
from transformers import pipeline

# Page Configuration
st.set_page_config(
    page_title="Local AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

# Custom CSS
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
    .stChatInputContainer {
        background-color: #f0f2f6 !important;
        border-radius: 12px;
        padding: 5px;
        border: 1px solid #d0d5dd;
    }
    #MainMenu, footer, header {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("Running locally on an open-source model (no API key).")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main Header
st.markdown(
    "<h1 style='text-align:center;color:#202123'>Local AI Assistant</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;color:#6e6e80'>"
    "Uses locally downloaded model weights without external AI APIs.</p>",
    unsafe_allow_html=True,
)

# Load the lightweight model once per app process.
@st.cache_resource
def load_model():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    with st.spinner("Loading local AI model..."):
        chatbot_pipeline = load_model()
except Exception as e:
    st.error(f"Could not load the model: {e}")
    st.info(
        "The first run needs internet access to download the model. "
        "Check your connection, disk space, and installed packages."
    )
    st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            try:
                # FLAN-T5 is not a chat-tuned model. Add a simple instruction
                # and recent turns as text context to make follow-ups clearer.
                recent = st.session_state.messages[-6:-1]
                context = "\n".join(
                    f"{'User' if m['role'] == 'user' else 'Assistant'}: "
                    f"{m['content']}"
                    for m in recent
                )
                model_input = (
                    "You are a helpful assistant. Answer the user's latest "
                    "message clearly. Use the conversation context if useful.\n"
                    f"{context}\nUser: {prompt}\nAssistant:"
                )
                outputs = chatbot_pipeline(
                    model_input,
                    max_new_tokens=150,
                    do_sample=False,
                )
                bot_response = outputs[0]["generated_text"].strip()
                st.markdown(bot_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": bot_response}
                )
            except Exception as e:
                st.error(f"Error generating response: {e}")
