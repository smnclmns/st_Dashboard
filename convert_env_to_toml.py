import os
from dotenv import load_dotenv
import toml

# .env-Datei laden
load_dotenv()

# Erstelle das .streamlit-Verzeichnis, falls es nicht existiert
os.makedirs('.streamlit', exist_ok=True)

# Erstelle eine Dictionary-Struktur für die .toml-Datei
config = {
    "connections": {
        "gsheets": {
            "spreadsheet": os.getenv("SPREADSHEET"),
            "worksheet": os.getenv("WORKSHEET"),
            "type": os.getenv("TYPE"),
            "project_id": os.getenv("PROJECT_ID"),
            "private_key_id": os.getenv("PRIVATE_KEY_ID"),
            "private_key": os.getenv("PRIVATE_KEY"),
            "client_email": os.getenv("CLIENT_EMAIL"),
            "client_id": os.getenv("CLIENT_ID"),
            "auth_uri": os.getenv("AUTH_URI"),
            "token_uri": os.getenv("TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
        }
    }
}

# Schreibe die Daten in eine .toml-Datei
with open('.streamlit/secrets.toml', 'w') as toml_file:
    toml.dump(config, toml_file)

print(".streamlit/secrets.toml file created successfully.")