"""Shared safety configuration — the ONE place to adjust before any run.

Every script imports from here, so there is a single DRY_RUN to flip
(and to remember to flip BACK to True afterward).
"""

# When True, destructive scripts only REPORT what they would trash/archive.
DRY_RUN = True

# Senders/domains to NEVER trash — add your important ones (bank, employer, etc.).
ALLOWLIST_SENDERS = [
    "walgreens.com",
]

# Terms that suggest transactional/important mail — excluded from trashing.
# Multi-word terms are quoted so Gmail treats them as phrases.
PROTECT_TERMS = [
    "receipt", "invoice", "statement", "payment", "refund",
    "verification", "password", "tax",
    "prescription", "refill", "pharmacy",
    '"security alert"', '"order confirmation"', '"shipping confirmation"',
]

# Unattended weekly run: refuse to trash if the query matches more than this.
MAX_TRASH = 500
