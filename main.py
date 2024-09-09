import streamlit as st

from streamlit_calendar import calendar
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth

from custom_moduls.Connection_handling import Connection_Handler
from custom_moduls.calender_widget import get_calender_options, get_calender_events, get_custom_css

# Set page configs
st.set_page_config(
    page_title="TamamTisch",
    page_icon=":100:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

    # ----- Main App Content -----

    # --- Calender ---

    calender_events = get_calender_events()
    calender_options = get_calender_options()
    calender_css = get_custom_css()
    
    calendar_instance = calendar(
        events=calender_events,
        options=calender_options,
        custom_css=calender_css,
    )

    st.write(calendar_instance)
