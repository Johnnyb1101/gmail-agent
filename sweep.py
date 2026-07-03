"""Moderate sweep: old bulk mail with unsubscribe links, with protections."""

from auth import get_gmail_service
from bulk_trash import list_all_ids, preview_subjects, batch_trash
from config import DRY_RUN, PROTECT_TERMS, ALLOWLIST_SENDERS


def build_query():
    """Assemble the Gmail search query with all protections applied."""
    parts = ["unsubscribe", "older_than:6m"]
    parts += [f"-{term}" for term in PROTECT_TERMS]      # exclude transactional terms
    parts += [f"-from:{s}" for s in ALLOWLIST_SENDERS]   # exclude trusted senders
    return " ".join(parts)


if __name__ == "__main__":
    service = get_gmail_service()
    query = build_query()

    print(f"\nQuery:\n{query}\n")
    ids = list_all_ids(service, query)
    print(f"Matched {len(ids):,} emails.\n")

    print("Sample of what would be trashed:")
    preview_subjects(service, ids, n=20)

    if DRY_RUN:
        print(f"\nDRY RUN — nothing trashed. Set DRY_RUN = False to trash these {len(ids):,}.")
    else:
        print(f"\nTrashing {len(ids):,} emails (recoverable)...")
        batch_trash(service, ids)
        print("Done. Moved to Trash — recoverable ~30 days.")