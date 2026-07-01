"""Read recent emails, then triage and summarize each with Claude."""

from auth import get_gmail_service
from gmail_reader import read_recent_emails
from summarizer import analyze_email
from labeler import get_or_create_label, apply_label   # <-- new


if __name__ == "__main__":
    service = get_gmail_service()
    emails = read_recent_emails(service, max_results=5)

    for i, email in enumerate(emails, start=1):
        result = analyze_email(email["subject"], email["snippet"])

        # Apply an "Agent/<Category>" label to this email.
        label_name = f"Agent/{result['category']}"
        label_id = get_or_create_label(service, label_name)
        apply_label(service, email["id"], label_id)

        print(f"\n--- Email {i} ---")
        print(f"From:     {email['sender']}")
        print(f"Subject:  {email['subject']}")
        print(f"Category: {result['category']}")
        print(f"Summary:  {result['summary']}")
        print(f"Labeled:  {label_name}")