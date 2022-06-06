from __future__ import print_function

import os.path
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from email.mime.text import MIMEText

SCOPES = ['https://mail.google.com/']


def gmail_send_message(creds):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    for guides on implementing OAuth2 for the application.
    """

    try:
        with open('candidates.csv', newline='') as csvfile:
            candidates = csv.reader(csvfile, delimiter=',', quotechar='|')
            for candidate in candidates:
                name = candidate[0]
                email = candidate[1]
                datahub_password = candidate[2]

                service = build('gmail', 'v1', credentials=creds)
                message = MIMEText("YOUR CONTENTS")
                message['To'] = f'{email}'
                message['From'] = 'YOUR EMAIL'
                message['Subject'] = ("YOUR SUBJECT")
                # encoded message
                encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
                    .decode()

                create_message = {
                    'raw': encoded_message
                }

                send_message = (
                    service.users().messages().send(
                        userId="YOUR EMAIL", body=create_message).execute()
                )
                print(f'message Result: {send_message}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None

    return send_message


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    gmail_send_message(creds)


if __name__ == '__main__':
    main()
