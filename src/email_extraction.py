import msal
import requests
import os
from flask import Flask, request, redirect
import configparser
import threading
from bs4 import BeautifulSoup
import re
from datetime import datetime
import logging
import datetime

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load configuration from config.cfg
config = configparser.ConfigParser()
config.read('config.cfg')

# App registration details from config file
CLIENT_ID = config.get('auth', 'CLIENT_ID')
CLIENT_SECRET = config.get('auth', 'CLIENT_SECRET')
TENANT_ID = config.get('auth', 'TENANT_ID')
REDIRECT_URI = config.get('auth', 'REDIRECT_URI')
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/Mail.Read"]
ENDPOINT = "https://graph.microsoft.com/v1.0/me/messages"

# Global variable to store the access token
access_token = None

@app.route("/")
def index():
    return "Email Extraction Service is running. Use /start-extraction to begin."

@app.route("/start-extraction")
def start_extraction():
    auth_url = _build_auth_url()
    print(f"Authentication URL: {auth_url}")
    return redirect(auth_url)

@app.route("/callback")
def callback():
    global access_token
    code = request.args.get("code")
    access_token = get_access_token(code)
    if access_token:
        threading.Thread(target=background_email_extraction).start()
        return "Authentication successful. Email extraction has started. You can close this window."
    else:
        return "Failed to authenticate. Please try again."

def _build_auth_url():
    return msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    ).get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)

def get_access_token(code):
    client = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    result = client.acquire_token_by_authorization_code(
        code, SCOPE, redirect_uri=REDIRECT_URI
    )
    
    if "access_token" in result:
        return result["access_token"]
    else:
        logging.error(f"Error getting access token: {result.get('error')} - {result.get('error_description')}")
        return None

def extract_emails():
    global access_token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    if os.path.exists("extracted_emails"):
        for file in os.listdir("extracted_emails"):
            file_path = os.path.join("extracted_emails", file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    else:
        os.makedirs("extracted_emails")

    params = {
        '$top': 50,
        '$select': 'subject,body,from,receivedDateTime'
    }

    # today = datetime.utcnow().date().isoformat()
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    params['$filter'] = f"receivedDateTime ge {today}T00:00:00Z and receivedDateTime le {today}T23:59:59Z"

    try:
        response = requests.get(ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        emails = response.json().get('value', [])
        
        for i, email in enumerate(emails):
            subject = email['subject']
            body = email['body']['content']
            sender = email['from']['emailAddress']['address']
            date = email['receivedDateTime']

            soup = BeautifulSoup(body, 'html.parser')
            for script_or_style in soup(['script', 'style']):
                script_or_style.decompose()
            plain_text_body = soup.get_text(separator='\n').strip()
            plain_text_body = re.sub(r'\b[A-Za-z0-9+/=]{100,}\b', '', plain_text_body)

            filename = f"extracted_emails/{i}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"From: {sender}\n")
                f.write(f"Date: {date}\n")
                f.write(f"Subject: {subject}\n\n")
                f.write(plain_text_body)

        print(f"Extracted {len(emails)} emails successfully!")
    except requests.RequestException as e:
        print(f"Error extracting emails: {str(e)}")

def background_email_extraction():
    extract_emails()

if __name__ == "__main__":
    app.run(port=5000)