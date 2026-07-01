"""Authenticate with the Gmail API and return a ready-to-use service object."""

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# What the agent is ALLOWED to do.
# gmail.modify = read, label, and trash - but it CANNOT permenatly delete emails.
# Deliberately never request the delete scope, so a permanent delete is not possible even if code had a bug.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_gmail_service():
    """Return an authenticated Gmail API service, loggin in if necessary."""
    creds = None

    # token.json holds your access after the first successful login.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If no valid saved login, get one.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Saved login expired but can be refreshed silently (no browser).
            creds.refresh(Request())
        else:
            # First run: open a browser so you can grant access.
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the login so future runs skip the browser step.
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

# This block only runs when you execute `python auth.py` directly.
# It is a quick self-test to prove the connection works.
if __name__ == "__main__":
    service = get_gmail_service()
    profile = service.users().getProfile(userId="me").execute()
    print(f"Logged in as {profile['emailAddress']}")
    print(f"Total messages in mailbox: {profile['messagesTotal']}")