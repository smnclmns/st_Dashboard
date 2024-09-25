import streamlit as st

import services.calender_widget as cw

st.write("This is the calender page.")

# --- Calender ---
# TODO: Add customizable options for the timeline

cw.timeline(
    options=cw.get_timeline_options(
        months_ahead=18,
        height="500px",
    ),
)