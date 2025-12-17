import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ---------------- Files ----------------
USERS_FILE = "users.csv"
FILES_FILE = "userfiles.csv"

# ---------------- Create CSV files if not exist ----------------
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["userid", "username", "password"]).to_csv(
        USERS_FILE, index=False
    )

if not os.path.exists(FILES_FILE):
    pd.DataFrame(columns=["userid", "filename", "datetime"]).to_csv(
        FILES_FILE, index=False
    )

# ---------------- Helper Functions ----------------
def load_users():
    return pd.read_csv(USERS_FILE, dtype=str)

def save_user(username, password):
    users = load_users()
    userid = len(users) + 1

    users.loc[len(users)] = [
        userid,
        username.strip(),
        password.strip()
    ]

    users.to_csv(USERS_FILE, index=False)

def authenticate(username, password):
    users = load_users()

    users["username"] = users["username"].str.strip()
    users["password"] = users["password"].str.strip()

    username = username.strip()
    password = password.strip()

    user = users[
        (users["username"] == username) &
        (users["password"] == password)
    ]

    return None if user.empty else user.iloc[0]

def save_history(userid, filename):
    history = pd.read_csv(FILES_FILE)

    history.loc[len(history)] = [
        userid,
        filename,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]

    history.to_csv(FILES_FILE, index=False)

# ---------------- Session State ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Menu")

    if not st.session_state.logged_in:
        mode = st.selectbox("Select Menu", ["Home", "Register", "Login"])
    else:
        mode = st.selectbox(
            "Select Menu",
            ["Explore CSV", "See History", "Logout"]
        )

# ---------------- Pages ----------------
if mode == "Home":
    st.title("Welcome")
    st.write("Please login or register to continue.")

elif mode == "Register":
    st.title("Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        users = load_users()
        if username.strip() in users["username"].values:
            st.error("Username already exists")
        else:
            save_user(username, password)
            st.success("Registration successful")

elif mode == "Login":
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(username, password)
        if user is not None:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

elif mode == "Explore CSV":
    st.title("Upload & Explore CSV")

    uploaded_file = st.file_uploader("Upload CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        save_history(
            st.session_state.user["userid"],
            uploaded_file.name
        )
        st.success("Upload history saved")

elif mode == "See History":
    st.title("CSV Upload History")

    history = pd.read_csv(FILES_FILE)
    user_history = history[
        history["userid"] == st.session_state.user["userid"]
    ]

    if user_history.empty:
        st.info("No uploads yet")
    else:
        st.dataframe(user_history)

elif mode == "Logout":
    st.session_state.logged_in = False
    st.session_state.user = None
    st.success("Logged out successfully")
    st.rerun()