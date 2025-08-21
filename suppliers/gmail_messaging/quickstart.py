import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

CREDS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH", "/run/secrets/gmail_credentials.json")
TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", "/run/secrets/gmail_token.json")
OAUTH_PORT = int(os.getenv("OAUTH_PORT", "8765"))

def generate_token():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(
                host="0.0.0.0",           
                port=OAUTH_PORT,         
                open_browser=False,       
                authorization_prompt_message=(
                    "\n[OAuth] Open the URL above in your browser to authorize, then return here.\n"
                ),
                success_message="[OAuth] Authorization complete. You can close this tab.",
            )
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    print(f"[OAuth] Token is ready at {TOKEN_PATH}")

if __name__ == "__main__":
    generate_token()
