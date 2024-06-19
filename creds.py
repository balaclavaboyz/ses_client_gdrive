import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials


def get_creds(scopes):
    creds = None
    if os.path.exists(r"c:\ses client\update_scripts_ib\token.json"):
        creds = Credentials.from_authorized_user_file(
            r"c:\ses client\update_scripts_ib\token.json", scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r"c:\ses client\update_scripts_ib\creds.json", scopes
            )
            creds = flow.run_local_server(port=0)

        with open(r"c:\ses client\update_scripts_ib\token.json", "w") as token:
            token.write(creds.to_json())

    return creds
