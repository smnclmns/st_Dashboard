import streamlit as st
from jinja2 import Template
from datetime import datetime
from custom_moduls.Connection_handling import ch

# Read the HTML template
with open("pages/templates/base.html", "r") as f:
    template = Template(f.read())

# Render the template with full-page layout
html_content = template.render(
    datetime=datetime,
    columns=ch.members_df.columns,
    data=ch.members_df,
)

# Use st.components.v1.html to render the HTML and use full width and height
st.components.v1.html(html_content, height=800, scrolling=True)
