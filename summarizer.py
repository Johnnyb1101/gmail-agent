"""Summarize an email with Claude (Haiku), after redacting sensitive information."""

from anthropic import Anthropic
from dotenv import load_dotenv

from redact import redact

# Load ANTHROPIC_API_KEY from .env file into environment.
load_dotenv()

# The client automatically reads ANTHROPIC_API_KEY from the environment.
client = Anthropic()

MODEL = "claude-haiku-4-5"


# The fixed set of categories Claude must choose from.
CATEGORIES = ["Promotions", "Newsletter", "Social", "Financial", "Personal", "Updates", "Other"]


def analyze_email(subject, snippet):
    """Return {'category': ..., 'summary': ...} for an email, redacting first."""
    safe_subject = redact(subject)
    safe_snippet = redact(snippet)

    prompt = (
        "You are triaging an email. Respond in EXACTLY this format, nothing else:\n"
        "CATEGORY: <one of: " + ", ".join(CATEGORIES) + ">\n"
        "SUMMARY: <one short factual sentence>\n\n"
        f"Subject: {safe_subject}\n"
        f"Preview: {safe_snippet}"
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text

    # Parse Claude's two labeled lines into a dict.
    category = "Other"
    summary = ""
    for line in text.splitlines():
        if line.startswith("CATEGORY:"):
            category = line.split(":", 1)[1].strip()
        elif line.startswith("SUMMARY:"):
            summary = line.split(":", 1)[1].strip()

    return {"category": category, "summary": summary}


if __name__ == "__main__":
    result = analyze_email(
        "Where will summer take you next with Hilton?",
        "Discover inspiring destinations, unforgettable stays, and new ways to explore with Hilton this summer.",
    )
    print(result)