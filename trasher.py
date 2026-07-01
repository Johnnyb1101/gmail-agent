"""Move emails to Trash (recoverable). Never permanently deletes."""


def trash_email(service, message_id):
    """Move a message to Trash. Recoverable for ~30 days. This is NOT a permanent delete."""
    service.users().messages().trash(userId="me", id=message_id).execute()