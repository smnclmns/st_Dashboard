# Description: This file contains the Connection_Handler class which is used to handle the connection to the google sheets
# and the credentials of the members. It is used to cache the connection and the credentials for 1 hour.

# Imported Moduls:
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_authenticator.utilities.hasher import Hasher
import pandas as pd

# Connection_Handler class

# @st.cache_resource(ttl=3600) # Cache for 1 hour
class Connection_Handler():
    def __init__(self):
        self.conn = st.connection("gsheets", GSheetsConnection)
        self.members_df = self.get_members_worksheet()
        self.credentials = self.get_credentials()
        self.spreadsheet_url = "https://docs.google.com/spreadsheets/d/1kio6yj57RyXq9miWRQZ-Y-ujscygOOCOv7EKudkI6P0/edit?gid=0#gid=0"

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
        return _insidecredentials
    
    def check_credentials(self, username: str, password: str) -> bool:
        '''
        Checks if the given username and password are correct.
        '''
        if username in self.credentials:
            if Hasher.check_pw(password, self.credentials[username]["password"]):
                st.session_state["name"] = self.credentials[username]["name"]
                st.session_state["authentication_status"] = True
                return True
            else:
                st.session_state["authentication_status"] = False
        else:
             st.session_state["authentication_status"] = False

        return False