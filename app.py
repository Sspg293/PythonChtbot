import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

st.set_page_config(
    page_title="Local AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.markdown("""
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
#MainMenu, footer, header {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ Settings")
    st.write("Running with an open-source language model")

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("Model: Microsoft Phi-3 Mini")

st.markdown(
    "<h1 style='text-align:center;color:#202123'>"
    "Local AI Assistant</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;color:#6e6e80'>"
    "Open-source AI chatbot</p>",
    unsafe_allow_html=True,
)

@st.cache_resource
def load_model():
    model_name = "microsoft/Phi-3-mini-4k-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype="auto",
    )
    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    with st.spinner("Loading AI model..."):
        chatbot = load_model()
except Exception as e:
    st.error(f"Could not load the model: {e}")
    st.info(
        "Check your internet connection, installed packages, "
        "available RAM, and model access."
    )
    st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Local AI..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Keep recent messages so the prompt stays within the model context.
    history = st.session_state.messages[-10:]
    chat_messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant. "
                "Answer clearly and accurately."
            ),
        }
    ] + history

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                prompt_text = chatbot.tokenizer.apply_chat_template(
                    chat_messages,
                    tokenize=False,
                    add_generation_prompt=True,
                )
                result = chatbot(
                    prompt_text,
                    max_new_tokens=512,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    return_full_text=False,
                )
                answer = result[0]["generated_text"].strip()
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as e:
                st.error(f"Response generation failed: {e}")
