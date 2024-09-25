import os
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

class Config:

    # General settings
    APP_NAME = "TamamTisch Dashboard"
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")

    # Paths and directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMP_DIR = os.path.join(BASE_DIR, '.temp')
    STATIC_DIR = os.path.join(BASE_DIR, 'static')

    # GSHEETS
    WORKSHEET = os.getenv('WORKSHEET')
    SPREADSHEET = os.getenv('SPREADSHEET')
    TYPE = os.getenv('TYPE')
    PROJECT_ID = os.getenv('PROJECT_ID')
    PRIVATE_KEY_ID = os.getenv('PRIVATE_KEY_ID')
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    CLIENT_EMAIL = os.getenv('CLIENT_EMAIL')
    CLIENT_ID = os.getenv('CLIENT_ID')
    AUTH_URI = os.getenv('AUTH_URI')
    TOKEN_URI = os.getenv('TOKEN_URI')
    AUTH_PROVIDER_X509_CERT_URL = os.getenv('AUTH_PROVIDER_X509_CERT_URL')
    CLIENT_X509_CERT_URL = os.getenv('CLIENT_X509_CERT_URL')

    # Streamlit-specific settings
    STREAMLIT_EMAIL = os.getenv("STREAMLIT_EMAIL", "simon2.clemens@tu-dortmund.de")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


if __name__ == "__main__":

    import toml

    # Erstelle das .streamlit-Verzeichnis, falls es nicht existiert
    os.makedirs('.streamlit', exist_ok=True)

    # Erstelle eine Dictionary-Struktur für die .toml-Datei
    env_keys = ["SPREADSHEET", "WORKSHEET", "TYPE", "PROJECT_ID", "PRIVATE_KEY_ID", "PRIVATE_KEY", "CLIENT_EMAIL", "CLIENT_ID", "AUTH_URI", "TOKEN_URI", "AUTH_PROVIDER_X509_CERT_URL", "CLIENT_X509_CERT_URL"]

    for key in env_keys:
        value = os.environ.get(key)
        # print(f"{key} = {value}")  # Debugging: Ausgeben der geladenen Variablen
        if value is None:
            raise ValueError(f"Environment variable {key} is not set.")

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