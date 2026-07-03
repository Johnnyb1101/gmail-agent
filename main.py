"""Read recent emails, then triage and summarize each with Claude."""

from auth import get_gmail_service
from gmail_reader import read_recent_emails
from summarizer import analyze_email
from labeler import get_or_create_label, apply_label
from trasher import trash_email
from config import DRY_RUN


# --- Safety configuration ---
BULK_CATEGORIES = {"Promotions", "Social", "Newsletter"}  # only these are trash candidates


if __name__ == "__main__":
    service = get_gmail_service()
    emails = read_recent_emails(service, max_results=5)

    for i, email in enumerate(emails, start=1):
        result = analyze_email(email["subject"], email["snippet"])

        label_name = f"Agent/{result['category']}"
        label_id = get_or_create_label(service, label_name)
        apply_label(service, email["id"], label_id)

        # Decide whether this is bulk mail to trash.
        if result["category"] in BULK_CATEGORIES:
            if DRY_RUN:
                action = "WOULD TRASH (dry run — nothing changed)"
            else:
                trash_email(service, email["id"])
                action = "TRASHED (moved to Bin, recoverable ~30 days)"
        else:
            action = "KEEP"

        print(f"\n--- Email {i} ---")
        print(f"From:     {email['sender']}")
        print(f"Subject:  {email['subject']}")
        print(f"Category: {result['category']}")
        print(f"Summary:  {result['summary']}")
        print(f"Labeled:  {label_name}")
        print(f"Action:   {action}")