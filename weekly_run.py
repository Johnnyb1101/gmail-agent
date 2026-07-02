"""Weekly maintenance run: trash new Promotions/Social mail, unattended.

Designed to be run by Windows Task Scheduler. Logs each run to weekly_run.log.
"""

import os
from datetime import datetime

# Make all relative paths (credentials.json, token.json, .env) resolve relative
# to THIS file, no matter what folder Task Scheduler launches us from.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from auth import get_gmail_service
from bulk_trash import list_all_ids, batch_trash

QUERY = "category:promotions OR category:social"
LOG_FILE = "weekly_run.log"


def log(message):
    """Append a timestamped line to the log file (and print it)."""
    line = f"{datetime.now():%Y-%m-%d %H:%M}  {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


if __name__ == "__main__":
    log("--- Weekly run started ---")
    try:
        service = get_gmail_service()
        ids = list_all_ids(service, QUERY)
        if ids:
            batch_trash(service, ids)
        log(f"Trashed {len(ids)} promotional/social emails.")
    except Exception as error:
        log(f"ERROR: {error}")
    log("--- Weekly run finished ---")