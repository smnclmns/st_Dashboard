import streamlit as st
from custom_moduls.Connection_handling import Connection_Handler

ch = Connection_Handler()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'authentication_status' in st.session_state:    
    if st.session_state.authentication_status == False:
        st.error("Name/Passwort ist falsch")
    elif st.session_state.authentication_status:
        st.success(f"Willkommen {st.session_state.name}")

def login():
    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            if ch.check_credentials(username, password):
                st.session_state.logged_in = True                
            st.rerun()

def logout():
    st.session_state.logged_in = False
    st.rerun()

logout_page = st.Page(logout, title="Logout", icon="🔓")

about_page = st.Page(
    page="views/about_us.py",
    title="About Us",
    icon="📜",
    default=True,
)

calender_page = st.Page(
    page="views/tamam_calender.py",
    title="Calender",
    icon="📅",
)

st.title("TamamTisch")

page_dict = {
    "About Us": [about_page],
    "Calender": [calender_page],
    "Logout": [logout_page],
}

if st.session_state.logged_in:
    pg = st.navigation(page_dict)
else:
    pg = st.navigation([st.Page(login, title="Login", icon="🔑")])

pg.run()