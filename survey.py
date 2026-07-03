"""Count how many emails match each Gmail search query (backlog survey)."""

from auth import get_gmail_service


def count_matching(service, query):
    """Count messages matching a query by paging through ALL results (accurate)."""
    total = 0
    page_token = None
    while True:
        response = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=500, pageToken=page_token)
            .execute(num_retries=3)
        )
        total += len(response.get("messages", []))
        page_token = response.get("nextPageToken")
        if not page_token:          # no more pages — we're done
            break
    return total


if __name__ == "__main__":
    service = get_gmail_service()

    # The true total comes from the profile, not a search estimate.
    profile = service.users().getProfile(userId="me").execute(num_retries=3)
    print("\n=== Inbox backlog survey ===")
    print(f"{'Total mailbox':22} {profile['messagesTotal']:>7,}")

    queries = {
        "Promotions tab":       "category:promotions",
        "Social tab":           "category:social",
        "Updates tab":          "category:updates",
        "Has unsubscribe link": "unsubscribe",
        "Unread":               "is:unread",
    }
    for label, query in queries.items():
        count = count_matching(service, query)
        print(f"{label:22} {count:>7,}")