"""Gmail OAuth2 Helper - Token management for IMAP access."""

import base64
import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# OAuth2 scopes for Gmail IMAP
SCOPES = ["https://mail.google.com/"]

# Token file path
TOKEN_FILE = Path(__file__).parent.parent / ".gmail_tokens.json"

# Client credentials (from n8n)
CLIENT_CONFIG = {
    "installed": {
        "client_id": "1078289465706-tpuet1lqt5ljqvtns0k9477tnj1pm7dh.apps.googleusercontent.com",
        "client_secret": "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",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"],
    }
}


def get_credentials() -> Credentials:
    """
    Get valid OAuth2 credentials, refreshing if necessary.

    Returns:
        Valid Credentials object.

    Raises:
        RuntimeError: If no valid credentials and can't refresh.
    """
    creds = None

    # Load existing tokens
    if TOKEN_FILE.exists():
        try:
            token_data = json.loads(TOKEN_FILE.read_text())
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except Exception as e:
            print(f"Warning: Could not load tokens: {e}")

    # Check if credentials are valid
    if creds and creds.valid:
        return creds

    # Try to refresh expired credentials
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _save_credentials(creds)
            return creds
        except Exception as e:
            print(f"Warning: Could not refresh token: {e}")

    # No valid credentials available
    raise RuntimeError("No valid OAuth2 credentials. Run 'python -m config.oauth_authorize' first.")


def authorize_interactive() -> Credentials:
    """
    Run interactive OAuth2 authorization flow.
    Opens browser for user consent.

    Returns:
        New Credentials object.
    """
    flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
    creds = flow.run_local_server(port=8080)
    _save_credentials(creds)
    return creds


def _save_credentials(creds: Credentials) -> None:
    """Save credentials to token file."""
    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
        "expiry": creds.expiry.isoformat() if creds.expiry else None,
    }
    TOKEN_FILE.write_text(json.dumps(token_data, indent=2))
    print(f"Credentials saved to {TOKEN_FILE}")


def get_oauth2_string(user: str) -> str:
    """
    Generate OAuth2 authentication string for IMAP.

    Args:
        user: Gmail email address.

    Returns:
        Base64-encoded OAuth2 string for IMAP AUTH.
    """
    creds = get_credentials()
    auth_string = f"user={user}\x01auth=Bearer {creds.token}\x01\x01"
    return base64.b64encode(auth_string.encode()).decode()
