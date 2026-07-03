"""Create and apply Gmail labels."""


def get_or_create_label(service, name):
    """Return the ID of a label with this name, creating it if it doesn't exist."""
    existing = service.users().labels().list(userId="me").execute(num_retries=3).get("labels", [])
    for label in existing:
        if label["name"] == name:
            return label["id"]

    # Not found — create it.
    created = (
        service.users()
        .labels()
        .create(
            userId="me",
            body={
                "name": name,
                "labelListVisibility": "labelShow",
                "messageListVisibility": "show",
            },
        )
        .execute(num_retries=3)
    )
    return created["id"]


def apply_label(service, message_id, label_id):
    """Add a label to a message (does not remove any existing labels)."""
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"addLabelIds": [label_id]},
    ).execute(num_retries=3)