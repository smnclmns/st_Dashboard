# Description: This file contains the Connection_Handler class which is used to handle the connection to the google sheets
# and the credentials of the members. It is used to cache the connection and the credentials for 1 hour.

# Imported Moduls:
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth
import pandas as pd
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

# Connection_Handler class

@st.cache_resource(ttl=3600) # Cache for 1 hour
class Connection_Handler():
    def __init__(self):
        self.conn = st.connection("gsheets", GSheetsConnection)
        self.members_df = self.get_members_worksheet()
        self.credentials = self.get_credentials()
        self.spreadsheet_url = os.getenv("SPREADSHEET")

    def get_members_worksheet(self) -> pd.DataFrame:
        '''
        Returns the members worksheet as a pandas DataFrame.
        '''
        members_df = self.conn.read(worksheet="Mitglieder")
        members_df["WhatsApp-Nr."] = members_df["WhatsApp-Nr."].astype(int).astype(str)
        return members_df
    
    def get_credentials(self) -> dict:
        '''
        Returns the credentials as a dictionary.
        '''
        _insidecredentials = {}
        for username in self.members_df["Username"].tolist():
            _insidecredentials[username] = {
                "name": self.members_df[self.members_df["Username"] == username]["Name"].values[0],
                "password": self.members_df[self.members_df["Username"] == username]["Passwort"].values[0]
            }
        return dict(usernames=_insidecredentials)
    
    def redirect_to_google_sheet(self):
        '''
        Redirects the user to the google sheet.
        '''
        st.write(f'<a href="{self.spreadsheet_url}" target="_blank">Google Sheet</a>', unsafe_allow_html=True)