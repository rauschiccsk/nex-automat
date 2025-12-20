"""
Fix Telegram Bot - správny endpoint a parameter
"""
from pathlib import Path

BOT_FILE = Path("apps/nex-brain/telegram/bot.py")

OLD_CODE = '''            response = await client.post(
                f"{API_URL}/chat",
                json={
                    "message": user_message,
                    "tenant": tenant
                }
            )
            response.raise_for_status()
            data = response.json()
            answer = data.get("response", "Prepáčte, nepodarilo sa spracovať dotaz.")'''

NEW_CODE = '''            response = await client.post(
                f"{API_URL}/api/v1/chat",
                json={
                    "question": user_message,
                    "tenant": tenant
                }
            )
            response.raise_for_status()
            data = response.json()
            answer = data.get("answer", "Prepáčte, nepodarilo sa spracovať dotaz.")'''


def main():
    print("=" * 70)
    print("FIX: Telegram Bot - endpoint a parameter")
    print("=" * 70)

    if not BOT_FILE.exists():
        print(f"❌ Súbor neexistuje: {BOT_FILE}")
        return False

    content = BOT_FILE.read_text(encoding='utf-8')

    if OLD_CODE not in content:
        print("❌ Nenašiel som kód na opravu")
        print("   Možno už bol opravený?")
        return False

    new_content = content.replace(OLD_CODE, NEW_CODE)
    BOT_FILE.write_text(new_content, encoding='utf-8')

    print(f"✅ Opravený: {BOT_FILE}")
    print()
    print("ZMENY:")
    print("  - /chat → /api/v1/chat")
    print("  - message → question")
    print("  - response → answer")
    print()
    print("Reštartuj bot: python apps/nex-brain/telegram/bot.py")
    print("=" * 70)

    return True


if __name__ == "__main__":
    main()