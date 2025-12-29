import streamlit as st

with st.form(key="reg_form"):
    st.header("Registration Form")
    first_name = st.text_input(key="fname",label="First Name")
    last_name =st.text_input(key="lname",label="Last Name")
    age = st.slider("Age",10,100,25,1)
    addr = st.text_area("Address")
    submit_btn = st.form_submit_button("Submit",type="primary")

    #form submit handling must be done outside form 'with' block

    if submit_btn:
        err_message = ""
        is_error = False
    if not first_name:
        is_error = True
        err_message +="First Nme can not be empty.\n"

    if not last_name:
        is_error = True
        err_message +="Last Nme can not be empty"
    
    if not addr:
        is_error = True
        err_message +="Address can not be empty.\n"

    if is_error:
        st.error(err_message)
    
    else:
        message = f"Successfully Registered : {st.session_state['fname']} {st.session_state['lname']}.\n Age:{age} living at {addr}"

st.success(message)
