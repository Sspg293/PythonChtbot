import streamlit as st
from transformers import pipeline

st.set_page_config(
    page_title="Local AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #ffffff; color: #333333; }
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
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("⚙️ Settings")
    st.write("Open-source model hosted with Streamlit")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.markdown(
    "<h1 style='text-align:center;color:#202123'>Local AI Assistant</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;color:#6e6e80'>"
    "Powered by Google FLAN-T5 Small.</p>",
    unsafe_allow_html=True,
)

@st.cache_resource
def load_model():
    # FLAN-T5 is an encoder-decoder text-to-text model.
    # Pin transformers in requirements.txt to a release that supports this task.
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    with st.spinner("Loading AI model..."):
        chatbot_pipeline = load_model()
except Exception as e:
    st.error(f"Could not load the model: {e}")
    st.info(
        "Check the app's dependency versions and redeploy. "
        "The first launch also needs internet to download the model."
    )
    st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            try:
                recent = st.session_state.messages[-6:-1]
                context = "\n".join(
                    f"{'User' if m['role'] == 'user' else 'Assistant'}: "
                    f"{m['content']}"
                    for m in recent
                )
                model_input = (
                    "Answer helpfully and clearly. Use the conversation "
                    "context when relevant.\n"
                    f"{context}\nUser: {prompt}\nAssistant:"
                )
                outputs = chatbot_pipeline(
                    model_input,
                    max_new_tokens=150,
                    do_sample=False,
                )
                answer = outputs[0]["generated_text"].strip()
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as e:
                st.error(f"Error generating response: {e}")
