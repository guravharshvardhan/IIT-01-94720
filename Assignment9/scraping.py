import streamlit as st
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

load_dotenv()
chromedriver_autoinstaller.install()

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("groq_api")
)

def scrape_sunbeam(keywords):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        return None, f"ChromeDriver error: {e}"

    driver.get("https://www.sunbeaminfo.in/internship")
    wait = WebDriverWait(driver, 10)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
    except:
        driver.quit()
        return None, "Table failed to load. Website structure changed or blocking automation."

    time.sleep(2)
    tables = driver.find_elements(By.CSS_SELECTOR, "table")
    results = []

    for table in tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cols = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]
            if not cols:
                continue
            row_text = " ".join(cols).lower()
            if any(kw.lower() in row_text for kw in keywords):
                results.append(cols)

    driver.quit()
    return results, None

def WebScrapingApp():
    st.header("Web Scraping Agent - Sunbeam Internships")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask about internships…")

    if user_input:
        st.session_state.chat.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        prompt = f"""
        Extract up to 5 meaningful search keywords from this question.
        Return ONLY comma-separated words.

        Question: {user_input}
        """
        raw = llm.invoke(prompt).content.strip().lower()
        keywords = [k.strip() for k in raw.split(",") if k.strip()]
        if not keywords:
            keywords = user_input.split()[:3]

        results, error = scrape_sunbeam(keywords)

        with st.chat_message("assistant"):
            if error:
                st.error(f"❌ {error}")
                response = error
            else:
                st.write(f"**🔑 Keywords Used:** {keywords}")
                st.write("---")
                if results:
                    st.subheader("🎯 Matching Internships Found")
                    for row in results:
                        formatted = " | ".join([c if c else "-" for c in row])
                        st.write(formatted)
                        st.write("---")
                    response = f"Found {len(results)} matching results."
                else:
                    st.warning("No matching internships found.")
                    response = "No relevant match found."
            st.write(response)
        st.session_state.chat.append({"role": "assistant", "content": response})

WebScrapingApp()