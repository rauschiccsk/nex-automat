"""Email Activities - IMAP operations for fetching invoices."""

import email
from dataclasses import dataclass
from email.message import Message
from typing import Optional
import imaplib

from temporalio import activity

from config.settings import get_settings


@dataclass
class EmailAttachment:
    """Represents an email attachment."""
    filename: str
    content: bytes
    content_type: str


@dataclass
class EmailMessage:
    """Represents a fetched email with attachments."""
    uid: int
    subject: str
    sender: str
    date: str
    attachments: list[EmailAttachment]


def _get_imap_connection() -> imaplib.IMAP4_SSL:
    """Create IMAP connection with standard password authentication."""
    settings = get_settings()

    # Connect to IMAP server with SSL
    imap = imaplib.IMAP4_SSL(settings.imap_host, settings.imap_port)

    # Authenticate with username and password
    imap.login(settings.imap_user, settings.imap_password)

    return imap


@activity.defn
async def fetch_unread_emails() -> list[EmailMessage]:
    """
    Fetch unread emails from IMAP server.

    Returns:
        List of EmailMessage objects with PDF attachments.
    """
    settings = get_settings()
    messages: list[EmailMessage] = []

    activity.logger.info(f"Connecting to {settings.imap_host}...")

    try:
        imap = _get_imap_connection()
        imap.select(settings.imap_folder)

        # Search for unread emails
        status, data = imap.search(None, "UNSEEN")
        if status != "OK":
            activity.logger.warning("Failed to search emails")
            return messages

        uids = data[0].split()
        activity.logger.info(f"Found {len(uids)} unread emails")

        if not uids:
            imap.logout()
            return messages

        # Fetch email data
        for uid in uids:
            status, msg_data = imap.fetch(uid, "(RFC822)")
            if status != "OK":
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Extract PDF attachments
            attachments = _extract_pdf_attachments(msg)

            if attachments:
                email_msg = EmailMessage(
                    uid=int(uid),
                    subject=msg.get("Subject", ""),
                    sender=msg.get("From", ""),
                    date=msg.get("Date", ""),
                    attachments=attachments
                )
                messages.append(email_msg)
                activity.logger.info(
                    f"Email UID {uid}: {len(attachments)} PDF attachment(s)"
                )

        imap.logout()

    except Exception as e:
        activity.logger.error(f"IMAP error: {e}")
        raise

    return messages


@activity.defn
async def mark_email_processed(uid: int) -> bool:
    """
    Mark email as processed (read) in IMAP.

    Args:
        uid: Email UID to mark as read.

    Returns:
        True if successful.
    """
    settings = get_settings()

    activity.logger.info(f"Marking email UID {uid} as processed...")

    try:
        imap = _get_imap_connection()
        imap.select(settings.imap_folder)

        # Add SEEN flag
        imap.store(str(uid).encode(), "+FLAGS", r"(\Seen)")
        activity.logger.info(f"Email UID {uid} marked as read")

        imap.logout()

    except Exception as e:
        activity.logger.error(f"Failed to mark email: {e}")
        raise

    return True


def _extract_pdf_attachments(msg: Message) -> list[EmailAttachment]:
    """Extract PDF attachments from email message."""
    attachments: list[EmailAttachment] = []

    for part in msg.walk():
        content_type = part.get_content_type()
        filename = part.get_filename()

        if filename and content_type == "application/pdf":
            content = part.get_payload(decode=True)
            if content:
                attachments.append(EmailAttachment(
                    filename=filename,
                    content=content,
                    content_type=content_type
                ))

    return attachments