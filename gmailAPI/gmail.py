import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import base64
from collections import defaultdict


def create_service(client_secret_file, api_name, api_version, *scopes, prefix=""):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    creds = None
    working_dir = os.getcwd()
    token_dir = "token files"
    token_file = f"token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.json"

    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
        creds = Credentials.from_authorized_user_file(
            os.path.join(working_dir, token_dir, token_file), SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(os.path.join(working_dir, token_dir, token_file), "w") as token:
            token.write(creds.to_json())

    try:
        service = build(
            API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False
        )
        print(API_SERVICE_NAME, API_VERSION, "service created successfully")
        return service
    except Exception as e:
        print(e)
        print(f"Failed to create service instance for {API_SERVICE_NAME}")
        os.remove(os.path.join(working_dir, token_dir, token_file))
        return None


"""def init_gmail_service(
    client_file, api_name="gmail", api_version="v1", scopes=["https://mail.google.com/"]
):
    return create_service(client_file, api_name, api_version, scopes)



#   READING EMAILS     


service = init_gmail_service("client_secret_desk.json")
"""

"""
def list_emails_grouped_by_thread(service, max_results=20):
    try:
        results = (
            service.users()
            .messages()
            .list(userId="me", maxResults=max_results)
            .execute()
        )
        messages = results.get("messages", [])

        threads = defaultdict(list)

        for msg in messages:
            msg_id = msg["id"]
            msg_data = (
                service.users()
                .messages()
                .get(userId="me", id=msg_id, format="full")
                .execute()
            )

            headers = msg_data["payload"]["headers"]
            parts = msg_data["payload"].get("parts", [])
            body_data = ""

            if parts:
                for part in parts:
                    if part["mimeType"] == "text/plain":
                        body_data = base64.urlsafe_b64decode(
                            part["body"]["data"]
                        ).decode("utf-8")
                        break
                    elif part["mimeType"] == "text/html":
                        body_data = base64.urlsafe_b64decode(
                            part["body"]["data"]
                        ).decode("utf-8")
                        break
            else:
                if "data" in msg_data["payload"]["body"]:
                    body_data = base64.urlsafe_b64decode(
                        msg_data["payload"]["body"]["data"]
                    ).decode("utf-8")

            email_info = {
                "id": msg_id,
                "threadId": msg_data["threadId"],
                "from": next((h["value"] for h in headers if h["name"] == "From"), ""),
                "subject": next(
                    (h["value"] for h in headers if h["name"] == "Subject"), ""
                ),
                "date": next((h["value"] for h in headers if h["name"] == "Date"), ""),
                "body": body_data.strip(),
            }

            threads[email_info["threadId"]].append(email_info)

        return threads

    except Exception as e:
        print("An error occurred:", e)
        return {}


# Usage
conversations = list_emails_grouped_by_thread(service, max_results=20)

# Print grouped conversations
for thread_id, emails in conversations.items():
    print(f"\n===== Conversation Thread ID: {thread_id} =====")
    for email in emails:
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Date: {email['date']}")
        print(f"Body:\n{email['body']}\n{'-'*80}")"""
