import streamlit as st

st.title("hello streamlit!")
st.header("welcome to GenAi training program!")
st.write("hello students ihope the session isgoing well...")

if st.button("click me",type="primary"):
    st.toast("you clicked me..")