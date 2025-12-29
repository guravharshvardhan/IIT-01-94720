import sql_queries as lwc
from scraping import WebScrapingApp
import streamlit as st
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("groq_api")
)

if "page" not in st.session_state:
    st.session_state.page = "csv"
if "msg_csv" not in st.session_state:
    st.session_state.msg_csv = []
if "msg_web" not in st.session_state:
    st.session_state.msg_web = []

st.title("2 Agent Application")
with st.sidebar:
    if st.button("CSV Agent", use_container_width=True):
        st.session_state.page = "csv"
    if st.button("Web Scraping Agent", use_container_width=True):
        st.session_state.page = "web"

if st.session_state.page == "csv":
    lwc.CSVApp()

if st.session_state.page == "web":
    WebScrapingApp()