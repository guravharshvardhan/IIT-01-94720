import streamlit as st
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
import pandas as pd
import pandasql as ps
load_dotenv()

llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("groq_api")
)

def CSVApp():
    csv_file =  st.file_uploader("Upload a CSV file", type=["csv"])
    if csv_file is not None:
        df = pd.read_csv(csv_file)
        st.write("CSV schema: ")
        st.dataframe(df)
        user_input = st.chat_input("Ask anything about this CSV? ")
        if user_input:
            llm_input = f"""
                Table Name: data
                Table Schema: {df}
                Question: {user_input}
                Instruction:
                    Write a SQL query for the above question. 
                    Generate SQL query only in plain text format and nothing else.
                    If you cannot generate the query, then output 'Error'.
            """
            query = llm.invoke(llm_input)
            st.write(query.content)
            if query.content == "Error":
                st.write("Error")

            else:
                result = ps.sqldf(query.content, {"data": df})
                st.write("\nQuery Result:")
                st.write(result)
                
                prompt = f"""
                            user question: {user_input}
                            generated querry: {query.content}
                            result: {result}
                            task:
                            explain the result in simple english, 
                            dont use sql langauge, 
                            keep it understandable for some one who dont know sql at all.
                            """
                explanation = llm.invoke(prompt)
                st.write("Explanation")
                st.write(explanation.content)