from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os


load_dotenv()


llm=init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"))

conversation=[]
while True:
    user_input=input("you:")
    if user_input == "exit":
        break

    user_msg={"role":"user","content":user_input}
    conversation.append(user_msg)
    llm_output=llm.invoke(conversation)
    print("AI:",llm_output.content)
    llm_msg={"role":"assistant","content":llm_output}
    conversation.append(llm_msg)