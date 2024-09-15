import streamlit as st
from jinja2 import Template

# Set page configs
st.set_page_config(
    page_title="TamamTisch",
    page_icon=":100:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Read the HTML template
with open("pages/templates/base.html", "r") as f:
    template = Template(f.read())

# Render the template with full-page layout
html_content = template.render()

# Use st.components.v1.html to render the HTML and use full width and height
st.components.v1.html(html_content, height=800, scrolling=True)
