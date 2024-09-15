import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth

@st.cache_resource(ttl=3600) # Cache for 1 hour
class Connection_Handler():
    def __init__(self):
        self.conn = st.connection("gsheets", GSheetsConnection)
        self.members_df = self.get_members_worksheet()
        self.credentials = self.get_credentials()

    def get_members_worksheet(self):
        members_df = self.conn.read(worksheet="Mitglieder")
        members_df["WhatsApp-Nr."] = members_df["WhatsApp-Nr."].astype(int).astype(str)
        return members_df
    
    def get_credentials(self):
        _insidecredentials = {}
        for username in self.members_df["Username"].tolist():
            _insidecredentials[username] = {
                "name": self.members_df[self.members_df["Username"] == username]["Name"].values[0],
                "password": self.members_df[self.members_df["Username"] == username]["Passwort"].values[0]
            }
        return dict(usernames=_insidecredentials)