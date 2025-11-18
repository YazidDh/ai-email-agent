from mcp.server.fastmcp import FastMCP

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from gmailAPI.gmail import create_service
app = FastMCP("gmail_mcp")

service = create_service(
        "client_secret_desk.json",
        "gmail",
        "v1",
        ["https://www.googleapis.com/auth/gmail.readonly"]
    )

def fetch_conversation(thread_id: str, service):
    """Fetches and formats a Gmail conversation by thread ID."""
  
 

    thread = service.users().threads().get(userId='me', id=thread_id).execute()
    messages = thread.get("messages", [])
    formatted_thread = ""

    for i, msg in enumerate(messages, 1):
        payload = msg.get("payload", {})
        headers = {h["name"]: h["value"] for h in payload.get("headers", [])}
        sender = headers.get("From", "Unknown Sender")
        subject = headers.get("Subject", "")
        snippet = msg.get("snippet", "")
        formatted_thread += f"\n--- Message {i} ---\nFrom: {sender}\nSubject: {subject}\nContent: {snippet}\n"

    return formatted_thread.strip()


@app.tool()
async def get_conversation(thread_id: str) -> str:
    """
    Retrieve and format a Gmail thread using its thread ID.
    Args:
        thread_id: Gmail thread ID
    Returns:
        Formatted string of all messages in that thread.
    """
    return fetch_conversation(thread_id, service)


if __name__ == "__main__":
    app.run()
