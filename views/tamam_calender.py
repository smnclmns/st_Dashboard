import streamlit as st

import services.calender_widget as cw

st.write("This is the calender page.")

# --- Calender ---
# TODO: Add customizable options for the timeline

cw.timeline(options=cw.get_timeline_options(
    height="500px",
    )
)