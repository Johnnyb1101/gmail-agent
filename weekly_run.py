"""Weekly maintenance run: trash new Promotions/Social mail, unattended.

Designed to be run by Windows Task Scheduler. Logs each run to weekly_run.log.
"""

import os
import sys
import traceback
from datetime import datetime

# Make all relative paths (credentials.json, token.json, .env) resolve relative
# to THIS file, no matter what folder Task Scheduler launches us from.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from auth import get_gmail_service
from bulk_trash import list_all_ids, batch_trash
from config import PROTECT_TERMS, ALLOWLIST_SENDERS, MAX_TRASH

LOG_FILE = "weekly_run.log"


def build_query():
    """Promotions/Social mail, minus the same protections the sweeps use."""
    # Parentheses matter: exclusions must apply to BOTH categories,
    # not just the second one.
    parts = ["(category:promotions OR category:social)"]
    parts += [f"-{term}" for term in PROTECT_TERMS]      # exclude transactional terms
    parts += [f"-from:{s}" for s in ALLOWLIST_SENDERS]   # exclude trusted senders
    return " ".join(parts)


def log(message):
    """Append a timestamped line to the log file (and print it)."""
    line = f"{datetime.now():%Y-%m-%d %H:%M}  {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


if __name__ == "__main__":
    log("--- Weekly run started ---")
    try:
        service = get_gmail_service(interactive=False)
        ids = list_all_ids(service, build_query())
        if len(ids) > MAX_TRASH:
            log(f"SAFETY STOP: matched {len(ids)} emails, cap is {MAX_TRASH}. Nothing trashed.")
            sys.exit(1)
        if ids:
            batch_trash(service, ids)
        log(f"Trashed {len(ids)} promotional/social emails.")
    except Exception:
        # Full stack trace, not just the message — shows WHERE it failed.
        log(f"ERROR:\n{traceback.format_exc()}")
        log("--- Weekly run FAILED ---")
        # Non-zero exit code tells Task Scheduler this run failed.
        sys.exit(1)
    log("--- Weekly run finished ---")