"""OAuth2 Authorization Script - Run once to authorize Gmail access."""

from config.gmail_oauth import TOKEN_FILE, authorize_interactive


def main():
    print("Gmail OAuth2 Authorization")
    print("=" * 40)
    print()
    print("This will open a browser window for Google sign-in.")
    print("Sign in with: magerstavinvoice@gmail.com")
    print()

    input("Press Enter to continue...")

    creds = authorize_interactive()

    print()
    print("✅ Authorization successful!")
    print(f"   Tokens saved to: {TOKEN_FILE}")
    print()
    print("You can now run the worker.")


if __name__ == "__main__":
    main()
