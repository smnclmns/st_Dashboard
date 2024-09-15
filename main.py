import streamlit as st

import streamlit_authenticator as stauth
from custom_moduls.streamlit_timeline import st_timeline

from dotenv import load_dotenv
import os

from custom_moduls.Connection_handling import Connection_Handler
from custom_moduls.calender_widget import get_tamam_member_calender_events, get_groups_from_members_df, get_timeline_options

# Load environment variables
load_dotenv()

# Set page configs
st.set_page_config(
    page_title="TamamTisch",
    page_icon=":100:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Create a connection object
ch = Connection_Handler()

# --- User Authentication ---

authenticator = stauth.Authenticate(ch.credentials, "TamamTisch", "bankenkratzenanwolken", 1, auto_hash=False)

authenticator.login()

if st.session_state["authentication_status"] == None:
    st.warning("Gib was ein")

elif st.session_state["authentication_status"] == False:
    st.error("Name/Passwort ist falsch")

elif st.session_state["authentication_status"]:
    authenticator.logout(location="sidebar")
    st.success(f"Willkommen {st.session_state['name']}")

    # ----- Main App Content -----

    # st.link_button("Google Sheet", os.getenv("SPREADSHEET"))

    # --- Calender ---
    
    events = get_tamam_member_calender_events(members_df=ch.members_df)
    groups = get_groups_from_members_df(members_df=ch.members_df)
    
    # Option variables
    # TODO: Make these variables user-configurable to dynamically change the timeline
    months_ahead = 18

    st_timeline(
        items=events,
        groups=groups,
        options=get_timeline_options(
            months_ahead=months_ahead,
        ),
        height="600px",
    )
    
