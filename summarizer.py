"""Summarize an email with Claude (Haiku), after redacting sensitive information."""

from anthropic import Anthropic
from dotenv import load_dotenv

from redact import redact

# Load ANTHROPIC_API_KEY from .env file into environment.
load_dotenv()

# The client automatically reads ANTHROPIC_API_KEY from the environment.
client = Anthropic()

MODEL = "claude-haiku-4-5"


def summarize_email(subject, snippet):
    """Return a short summary of an email, redacting sensitive info first."""
    # Redact BEFORE building the prompt - nothing sensitive reaches Claude.
    safe_subject = redact(subject)
    safe_snippet = redact(snippet)

    prompt = (
        "Summarize this email in one short sentence. Be concise and factual.\n\n"
        f"Subject: {safe_subject}\n"
        f"Preview: {safe_snippet}"
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )

    # The response text lives in the first content block.
    return response.content[0].text


if __name__ == "__main__":
    summary = summarize_email(
        "Where will summer take you next with Hilton?",
        "Discover inspiring destinations, unforgettable stays, and new ways to explore with Hilton this summer.",
    )
    print(f"Summary: {summary}")