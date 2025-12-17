import streamlit as st
import time

st.title("💬 Chatbot UI")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to stream text with delay
def stream_reply(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.2)

# Display previous messages
for role, msg in st.session_state.messages:
    if role == "user":
        st.write(f"👤 You: {msg}")
    else:
        st.write(f"🤖 Bot: {msg}")

# User input
user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    # Save user message
    st.session_state.messages.append(("user", user_input))

    # Bot reply (fake echo reply)
    bot_reply = f"You said '{user_input}'. Nice to chat with you!"

    # Display streaming reply
    st.write("🤖 Bot:")
    st.write_stream(stream_reply(bot_reply))

    # Save bot reply
    st.session_state.messages.append(("bot", bot_reply))

    st.rerun()
