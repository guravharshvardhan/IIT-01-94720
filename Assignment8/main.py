import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import requests, os



load_dotenv()
API_KEY = os.getenv("open_weather")


#Tools
@tool
def calculator(expression: str) -> str:
    """Evaluate math."""
    try:
        return str(eval(expression))
    except:
        return "Error: invalid expression"


@tool
def current_weather(city: str) -> str:
    """ The Current Weather """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        r = requests.get(url)
        data = r.json()

        if data.get("cod") != 200:
            return f"Weather error: {data.get('message', 'Unknown')}"
        
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"{city}: {temp}°C, {desc}"
    except Exception as e:
        return f"Weather error: {e}"


@tool
def knowledge_lookup(query: str) -> str:
    """Quick fact lookup."""
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        data = requests.get(url, timeout=5).json()
        return data.get("Abstract", "No clear answer found.")
    except Exception as e:
        return f"Lookup error: {e}"


# Model & Agents
llm = init_chat_model(
    model="meta-llama-3.1-8b-instruct",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy"
)

agent = create_agent(
    model=llm,
    tools=[calculator, current_weather, knowledge_lookup],
    system_prompt="""
Strict tool agent. Rules:
- If math → calculator
- If weather → current_weather
- If who/what/when/where/why → knowledge_lookup
- No tool explanation, just final result.
"""
)


# Streamlit
st.title(" AI Tool Chatbot")
st.caption("Uses tools for math, weather & knowledge lookup")


# Session state
if "chat" not in st.session_state:
    st.session_state.chat = []

if "file_content" not in st.session_state:
    st.session_state.file_content = None

# Chat history
for msg in st.session_state.chat:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])



# File upload
uploaded_file = st.file_uploader("Upload a file:", type=["txt", "csv", "json"])

if uploaded_file:
    try:
        st.session_state.file_content = uploaded_file.read().decode("utf-8")
        st.subheader(" File Content:")
        st.code(st.session_state.file_content)
    except:
        st.error(" Invalid text file or encoding.")


# User Input
user_msg = st.chat_input("Type your message...")

if user_msg:
   
    with st.chat_message("user"):
        st.write(user_msg)
    
    st.session_state.chat.append(
        {
            "role":"user",
            "content":user_msg
        }
    )

    try:
        result = agent.invoke(
            {
                "messages":
                [
                    {
                        "role": "user", 
                        "content": user_msg
                    }
                ]
            }
        )

        reply = result["messages"][-1].content

    except Exception as e:
        reply = f"Agent Error: {e}"

   
    with st.chat_message("assistant"):
        st.write(reply)

    st.session_state.chat.append(
        {
            "role":"assistant",
            "content":reply
        }
    )