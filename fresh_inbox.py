"""One-time fresh start: trash remaining marketing, archive the rest of the old inbox.

- Marketing (unsubscribe, minus transactional protections + allowlist) -> Trash (recoverable 30d)
- Everything else still in the inbox, older than ARCHIVE_OLDER_THAN     -> Archive (kept, searchable)
"""

from auth import get_gmail_service
from bulk_trash import list_all_ids, preview_subjects, batch_trash, batch_archive
from config import DRY_RUN, PROTECT_TERMS, ALLOWLIST_SENDERS

# Keep mail newer than this in the inbox; archive older. "0d" would archive everything.
ARCHIVE_OLDER_THAN = "1m"


def marketing_query():
    """Marketing mail of ALL ages, minus transactional protections + allowlist."""
    parts = ["unsubscribe"]
    parts += [f"-{term}" for term in PROTECT_TERMS]
    parts += [f"-from:{s}" for s in ALLOWLIST_SENDERS]
    return " ".join(parts)


if __name__ == "__main__":
    service = get_gmail_service()

    trash_q = marketing_query()
    archive_q = f"in:inbox older_than:{ARCHIVE_OLDER_THAN}"

    trash_ids = list_all_ids(service, trash_q)
    print(f"\n[1] TRASH marketing — matched {len(trash_ids):,}")
    print("    Sample:")
    preview_subjects(service, trash_ids, n=10)

    archive_ids = list_all_ids(service, archive_q)
    print(f"\n[2] ARCHIVE old inbox ({archive_q}) — matched {len(archive_ids):,}")

    if DRY_RUN:
        print("\nDRY RUN — nothing changed. Set DRY_RUN = False to execute.")
    else:
        print(f"\n[1] Trashing {len(trash_ids):,} marketing emails...")
        if trash_ids:
            batch_trash(service, trash_ids)
        # Re-fetch archive set AFTER trashing so we don't re-touch binned mail.
        archive_ids = list_all_ids(service, archive_q)
        print(f"\n[2] Archiving {len(archive_ids):,} old inbox emails...")
        if archive_ids:
            batch_archive(service, archive_ids)
        print("\nDone. Marketing trashed (recoverable 30d); the rest archived (in All Mail).")