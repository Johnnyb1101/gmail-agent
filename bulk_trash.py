"""Bulk-trash emails matching a Gmail query. Reversible (moves to Trash)."""

from auth import get_gmail_service


def list_all_ids(service, query):
    """Return every message ID matching a query (handles pagination)."""
    ids = []
    page_token = None
    while True:
        response = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=500, pageToken=page_token)
            .execute(num_retries=3)
        )
        ids.extend(m["id"] for m in response.get("messages", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return ids


def preview_subjects(service, ids, n=10):
    """Print sender + subject of the first n messages so you can eyeball the target."""
    for msg_id in ids[:n]:
        full = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=msg_id,
                format="metadata",
                metadataHeaders=["Subject", "From"],
            )
            .execute(num_retries=3)
        )
        # Defensive: not every message has a payload/headers (drafts, chat imports).
        headers = full.get("payload", {}).get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(no subject)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(no sender)")
        print(f"  - {sender[:38]:38} | {subject[:60]}")


def batch_trash(service, ids):
    """Move messages to Trash in batches of 1000 (reversible)."""
    for start in range(0, len(ids), 1000):
        chunk = ids[start:start + 1000]
        service.users().messages().batchModify(
            userId="me",
            body={"ids": chunk, "addLabelIds": ["TRASH"]},
        ).execute(num_retries=3)
        print(f"  Trashed {start + len(chunk):,} / {len(ids):,}")

def batch_archive(service, ids):
    """Remove messages from the Inbox (archive) in batches of 1000.
    Reversible, and NOTHING is deleted — mail stays in All Mail, searchable."""
    for start in range(0, len(ids), 1000):
        chunk = ids[start:start + 1000]
        service.users().messages().batchModify(
            userId="me",
            body={"ids": chunk, "removeLabelIds": ["INBOX"]},
        ).execute(num_retries=3)
        print(f"  Archived {start + len(chunk):,} / {len(ids):,}")


# --- Safety configuration ---
from config import DRY_RUN
QUERY = "category:promotions OR category:social"


if __name__ == "__main__":
    service = get_gmail_service()

    print(f"\nQuery: {QUERY}")
    ids = list_all_ids(service, QUERY)
    print(f"Matched {len(ids):,} emails.\n")

    print("Sample of what would be trashed:")
    preview_subjects(service, ids)

    if DRY_RUN:
        print(f"\nDRY RUN — nothing trashed. Set DRY_RUN = False to trash these {len(ids):,}.")
    else:
        print(f"\nTrashing {len(ids):,} emails (recoverable)...")
        batch_trash(service, ids)
        print("Done. All moved to Trash — recoverable ~30 days.")