from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth

class Connection_Handler():
    def __init__(self, conn: GSheetsConnection):
        self.conn = conn
        self.members_df = self.get_members_worksheet()

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