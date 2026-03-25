import requests
import streamlit as st

st.title("ChatBot")

mode_flag = st.toggle("Activate async chat", value=False)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Write your prompt in this input field"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.text(prompt)

    if mode_flag:
        response = requests.get(
            "http://localhost:8000/chat/async", params={"query": prompt}
        )
    else:
        response = requests.get(
            "http://localhost:8000/chat/sync", params={"query": prompt}
        )

    response.raise_for_status()

    response_text = (
        response.json()["response"]
        + f"\n\n**Response Mode**: {'Async' if mode_flag else 'Sync'}"
        + f"\n\n**Response Time**: {response.headers.get('X-Response-Time', 'N/A')} seconds"
    )
    
    st.session_state.messages.append({"role": "assistant", "content": response_text})

    with st.chat_message("assistant"):
        st.markdown(response_text)