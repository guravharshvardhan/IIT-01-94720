import streamlit as st
from dotenv import load_dotenv
import os
import requests

load_dotenv()
st.title("My Chatbot")

# ================== SESSION STATE ==================
if "cloud_history" not in st.session_state:
    st.session_state.cloud_history = []

if "local_history" not in st.session_state:
    st.session_state.local_history = []

# ================== GROQ CONFIG ==================
api_key = os.getenv("GROQ_API_KEY")
groq_url = "https://api.groq.com/openai/v1/chat/completions"
groq_headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Menu")
    mode = st.selectbox("Select Menu", ["Cloud Based API", "Local API"])
    if st.button("Clear Chat"):
        if mode == "Cloud Based API":
            st.session_state.cloud_history = []
        else:
            st.session_state.local_history = []
        st.rerun()

# ================== CLOUD (GROQ) ==================
if mode == "Cloud Based API":
    history = st.session_state.cloud_history

    # Show previous messages
    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask anything")

    if user_input:
        # Store user message
        history.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        req_data = {
            "model": "llama-3.3-70b-versatile",
            "messages": history
        }

        response = requests.post(groq_url, headers=groq_headers, json=req_data)

        if response.status_code != 200:
            st.error(f"HTTP Error {response.status_code}")
            st.code(response.text)
        else:
            res = response.json()
            if "choices" not in res:
                st.error("Groq API Error")
                st.json(res)
            else:
                reply = res["choices"][0]["message"]["content"]
                history.append({"role": "assistant", "content": reply})

                with st.chat_message("assistant"):
                    st.markdown(reply)

# ================== LOCAL (LM STUDIO) ==================
if mode == "Local API":
    history = st.session_state.local_history

    # Show previous messages
    for msg in history:
        if msg["role"]=="user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            st.markdown(msg["content"])

    lm_url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {
        "Authorization": "Bearer local",
        "Content-Type": "application/json"
    }

    user_input = st.chat_input("Ask anything")

    if user_input:
        history.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        req_data = {
            "model": "meta-llama-3.1-8b-instruct",
            "messages": history
        }

        response = requests.post(lm_url, headers=headers, json=req_data)

        if response.status_code != 200:
            st.error(f"HTTP Error {response.status_code}")
            st.code(response.text)
        else:
            res = response.json()
            if "choices" not in res:
                st.error("LM Studio API Error")
                st.json(res)
            else:
                reply = res["choices"][0]["message"]["content"]
                history.append({"role": "assistant", "content": reply})

                with st.chat_message("assistant"):
                    st.markdown(reply)