import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate_gmail():
    """Authenticate and return the Gmail API service."""
    creds = None
    if os.path.exists('./gmail/token.json'):
        creds = Credentials.from_authorized_user_file('./gmail/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './gmail/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('./gmail/token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_recent_emails(service, max_results=1):
    """Fetch the most recent emails."""
    results = service.users().messages().list(userId='me', maxResults=max_results, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    return messages


def get_email_details(service, user_id='me'):
    """Extract info from the email

    Args:
        service (_type_): _description_
        user_id (str, optional): _description_. Defaults to 'me'.

    Returns:
        _type_: _description_
    """
    results = service.users().messages().list(userId=user_id, labelIds=['INBOX'], q="is:unread", maxResults=1).execute()
    messages = results.get('messages', [])
    for message in messages:
        msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
        payload = msg['payload']
        headers = payload['headers']

        # Extract details
        email_data = {}
        for header in headers:
            if header['name'] == 'Date':
                email_data['date'] = header['value']
            elif header['name'] == 'From':
                email_data['from'] = header['value']
            elif header['name'] == 'Subject':
                email_data['subject'] = header['value']

        parts = payload.get('parts', [])
        if parts:
            body = ''
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    body = part['body']['data']
                    body = base64.urlsafe_b64decode(body).decode('utf-8')
                    break
        else:
            body = None
           

        email_data['body'] = body
        return email_data
        


        
        

