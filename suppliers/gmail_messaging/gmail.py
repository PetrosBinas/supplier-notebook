import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# read from env (these are the *container* paths set by docker)
CREDS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH", "/run/secrets/gmail_credentials.json")
TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", "/run/secrets/gmail_token.json")
FROM_ADDRESS = os.getenv("GMAIL_FROM_ADDRESS")

class GmailSender:
    @staticmethod
    def _load_credentials():
        creds = None
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds

    @staticmethod
    def send_gmail(contact: str, message_info: str, subject: str = "Supplier Order"):
        if not FROM_ADDRESS:
            raise RuntimeError("GMAIL_FROM_ADDRESS not set. Fill it in your .env.")

        creds = GmailSender._load_credentials()
        if not creds:
            raise RuntimeError("Gmail token not found. Run the Docker quickstart to create token.json.")

        try:
            service = build("gmail", "v1", credentials=creds)
            message = EmailMessage()
            message.set_content(message_info)
            message["TO"] = contact
            message["FROM"] = FROM_ADDRESS
            message["SUBJECT"] = subject

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {"raw": encoded_message}

            send_result = service.users().messages().send(userId="me", body=create_message).execute()
            print(f"[Gmail] Message Id: {send_result.get('id')}")
            return send_result
        except HttpError as error:
            print(f"[Gmail] Error: {error}")
            return None
