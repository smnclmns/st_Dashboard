import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth

# Create a connection object
conn = st.connection("gsheets", GSheetsConnection)
members_df = conn.read(worksheet="Mitglieder")

# --- User Authentication ---
_insidecredentials = {}
for username in members_df["Username"].tolist():
    _insidecredentials[username] = {
        "name": members_df[members_df["Username"] == username]["Name"].values[0],
        "password": members_df[members_df["Username"] == username]["Passwort"].values[0]
    }
credentials = dict(usernames=_insidecredentials)

authenticator = stauth.Authenticate(credentials, "TamamTisch", "bankenkratzenanwolken", 1, auto_hash=False)

authenticator.login()

if st.session_state["authentication_status"] == None:
    st.warning("Gib was ein")

elif st.session_state["authentication_status"] == False:
    st.error("Name/Passwort ist falsch")

elif st.session_state["authentication_status"]:
    authenticator.logout(location="sidebar")
    st.success(f"Willkommen {st.session_state['name']}")

    st.dataframe(members_df.drop(columns="Passwort"))