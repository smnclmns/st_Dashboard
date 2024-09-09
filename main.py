import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth
from custom_moduls.Connection_handling import Connection_Handler

# Create a connection object
conn = st.connection("gsheets", GSheetsConnection)
ch = Connection_Handler(conn)

# --- User Authentication ---
credentials = ch.get_credentials()

authenticator = stauth.Authenticate(credentials, "TamamTisch", "bankenkratzenanwolken", 1, auto_hash=False)

authenticator.login()

if st.session_state["authentication_status"] == None:
    st.warning("Gib was ein")

elif st.session_state["authentication_status"] == False:
    st.error("Name/Passwort ist falsch")

elif st.session_state["authentication_status"]:
    authenticator.logout(location="sidebar")
    st.success(f"Willkommen {st.session_state['name']}")

    st.dataframe(ch.members_df.drop(columns="Passwort"))

    calender_file = st.file_uploader("Datei hochladen")