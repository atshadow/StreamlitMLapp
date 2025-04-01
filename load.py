import streamlit as st
import subprocess
def authenticate(email, password):
    # Predefined user credentials (Modify as needed)
    valid_email = "user@example.com"
    valid_password = "password123"
    return email == valid_email and password == valid_password

# Session state to track login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("Login Page")

if not st.session_state.logged_in:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if authenticate(email, password):
            st.session_state.logged_in = True
            st.success("Login successful! Redirecting...")
            st.rerun()  # Refresh to update session state
        else:
            st.error("Invalid email or password")
else:
    st.success("You are logged in!")
    
    if st.button("Go to Health Assistant"):
        st.session_state.logged_in = True
        subprocess.run(["streamlit", "run", "app.py"])

    st.rerun()
