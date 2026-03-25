from typing import Iterable

import requests
import streamlit as st

st.title("ChatBot")

def decoded_chunks() -> Iterable[str]:
    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        if chunk:
            yield chunk

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Write your prompt in this input field"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.text(prompt)
        
    with st.spinner("Thinking...", show_time=True):
        response = requests.post(
            "http://localhost:8000/chat/stream", json={"query": prompt}, stream=True
        )

    response.raise_for_status()

    with st.chat_message("assistant"):
        response_text = st.write_stream(decoded_chunks())
        
        st.session_state.messages.append({"role": "assistant", "content": response_text})