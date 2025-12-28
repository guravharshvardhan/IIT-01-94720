import streamlit as st
import pandas as pd
import os
import dotenv
from langchain.chat_models import init_chat_model
import pandasql as ps

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Query Maker", layout="wide")
st.title(" QueryMaker")

dotenv.load_dotenv()

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# ------------------ SESSION STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "df" not in st.session_state:
    st.session_state.df = None

# ------------------ FILE UPLOAD ------------------
file = st.file_uploader("Upload CSV file", type="csv")

if file:
    st.session_state.df = pd.read_csv(file)
    st.success("CSV Uploaded Successfully")

    st.subheader(" Preview")
    st.dataframe(st.session_state.df.head())

    st.subheader(" Schema")
    st.code(str(st.session_state.df.dtypes))

# ------------------ CHAT HISTORY ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.code(msg["content"], language="sql")
        else:
            st.write(msg["content"])

# ------------------ USER INPUT ------------------
if st.session_state.df is not None:
    user = st.chat_input("Ask about this CSV...")

    if user:
        st.session_state.messages.append(
            {"role": "user", "content": user}
        )

        with st.chat_message("user"):
            st.write(user)

        prompt = f"""
Table name: data
Table schema: {st.session_state.df.dtypes}
Question: {user}

Instruction:
- Generate ONLY a SQL SELECT query
- Use table name exactly as `data`
- If not possible, return Error
"""

        with st.chat_message("assistant"):
            response = llm.invoke(prompt).content.strip()

            # Clean markdown
            response = response.replace("```sql", "").replace("```", "").strip()

            st.code(response, language="sql")

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

        # ------------------ EXECUTE SQL ------------------
        if not response.lower().startswith("select"):
            st.error(" Only SELECT queries are allowed")
        else:
            result = ps.sqldf(response, {"data": st.session_state.df})
            st.subheader(" Result")
            st.dataframe(result)


