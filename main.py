import streamlit as st
import pandas as pd
import numpy as np

st.title('Simons first streamlit app')

BA_data = pd.read_csv('BA_data.csv', sep=';')
st.write(BA_data)