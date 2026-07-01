"""Strip sensitive data from text before sending it to an external AI."""

import re

# Each entry is (pattern, replacement). Order matters — earlier patterns
# run first, so put the most specific shapes (cards) before general ones (long numbers).
PATTERNS = [
    # Credit-card-like: four groups of digits, optionally split by space or dash.
    (re.compile(r"\b(?:\d{4}[ -]?){3}\d{1,4}\b"), "[REDACTED_CARD]"),
    # US Social Security Number: 3-2-4 digits.
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[REDACTED_SSN]"),
    # Phone numbers: handles 555-123-4567, (555) 123-4567, +1 555 123 4567.
    (re.compile(r"\b(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}\b"), "[REDACTED_PHONE]"),
    # Email addresses.
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), "[REDACTED_EMAIL]"),
    # Any long run of digits (7+): account/order/reference numbers.
    (re.compile(r"\b\d{7,}\b"), "[REDACTED_NUMBER]"),
]


def redact(text):
    """Return text with sensitive patterns replaced by placeholders."""
    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    return text


# Self-test: run `python redact.py` to SEE what gets stripped.
if __name__ == "__main__":
    samples = [
        "Your card 4111 1111 1111 1111 was charged.",
        "SSN on file: 123-45-6789.",
        "Reply to john.doe@example.com or call 555-123-4567.",
        "Order #100482910 has shipped.",
        "Meeting at 3pm about the Q3 report.",  # nothing sensitive — should be untouched
    ]
    for s in samples:
        print(f"BEFORE: {s}")
        print(f"AFTER:  {redact(s)}\n")