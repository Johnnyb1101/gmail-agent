"""Read recent emails from Gmail."""

from auth import get_gmail_service

def get_header (headers, name):
    """Return the value of a header (e.g. 'Subject') from a message's header list."""
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""

def read_recent_emails(service, max_results=10):
    """Return recent emails as a list of dicts with sender, subject, and snippet."""
    # STEP 1: get a list of recent message IDs (this returns IDs only.)
    response = (
        service.users()
        .messages()
        .list(userId="me", maxResults=max_results)
        .execute()
    )
    messages = response.get("messages", [])

    emails = []
    # STEP 2: for each ID, fetch just the headers we care about + snippet.
    for message in messages:
        full = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=["From", "Subject"],
            )
            .execute()
        )

        # THIS is what was missing — save what we fetched into the list.
        headers = full["payload"]["headers"]
        emails.append(
            {
                "id": message["id"],
                "sender": get_header(headers, "From"),
                "subject": get_header(headers, "Subject"),
                "snippet": full.get("snippet", ""),
            }
        )

    return emails

if __name__ == "__main__":
    service = get_gmail_service()
    emails = read_recent_emails(service, max_results=10)
    for i, email in enumerate(emails, start=1):
        print(f"\n--- Email {i} ---")
        print(f"From: {email['sender']}")
        print(f"Subject: {email['subject']}")
        print(f"Preview: {email['snippet'][:100]}")