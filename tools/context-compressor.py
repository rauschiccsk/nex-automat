"""
Context Compressor - nex-automat projekt
Komprimuje históriu chatu pomocou Claude API
POZNÁMKA: Vyžaduje ANTHROPIC_API_KEY v config.py
"""

import sys
from datetime import datetime
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("❌ Chýba 'anthropic' package")
    print("   Nainštaluj: pip install anthropic")
    sys.exit(1)

try:
    from config import ANTHROPIC_API_KEY, SESSION_NOTES_DIR
except ImportError:
    print("❌ Chýba konfigurácia")
    print("   Vytvor config.py a nastav ANTHROPIC_API_KEY")
    sys.exit(1)


class ContextCompressor:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or ANTHROPIC_API_KEY

        if not self.api_key or self.api_key == "":
            raise ValueError("ANTHROPIC_API_KEY nie je nastavený v config.py")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.session_notes_dir = Path(SESSION_NOTES_DIR)

    def compress_chat_history(self, history_file: Path) -> str:
        """
        Skomprimuj históriu chatu do kompaktného zhrnutia

        Args:
            history_file: Cesta k súboru s históriou

        Returns:
            Komprimovaný text
        """

        if not history_file.exists():
            raise FileNotFoundError(f"Súbor neexistuje: {history_file}")

        # Načítaj históriu
        history = history_file.read_text(encoding="utf-8")
        history_length = len(history)

        print(f"\n📄 Komprimujem: {history_file.name}")
        print(f"📏 Pôvodná veľkosť: {history_length:,} znakov")

        # Vytvor prompt pre kompresia
        compression_prompt = f"""Analyzuj túto históriu konverzácie pre nex-automat projekt a vytvor ULTRA-KOMPAKTNÉ zhrnutie.

FORMÁT VÝSTUPU (maximálne 800 znakov):

## AKTUÁLNY STAV
[3-5 viet o tom kde sme skončili, čo je rozpracované]

## DOKONČENÉ ÚLOHY
• [Stručný bullet point]
• [Stručný bullet point]

## ĎALŠÍ KROK
[1 konkrétna veta - čo treba spraviť ako prvé]

## KRITICKÉ POZNÁMKY
[Len ak sú - dôležité detaily ktoré nesmieme stratiť]

HISTORICKÝ OBSAH:
{history}

POZNÁMKA: Odpovedaj IBA komprimovaným obsahom, žiadny úvod ani záver!"""

        print("🤖 Posielam na Claude API...")

        try:
            # Zavolaj Claude API
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                temperature=0.3,  # Nižšia temperatura = konzistentnejšie výsledky
                messages=[{"role": "user", "content": compression_prompt}],
            )

            # Extrahuj odpoveď
            compressed = message.content[0].text.strip()
            compressed_length = len(compressed)

            # Výpočet kompresie
            compression_ratio = (1 - compressed_length / history_length) * 100

            print(f"✅ Komprimované: {compressed_length:,} znakov")
            print(f"📊 Kompresia: {compression_ratio:.1f}%")

            # Ulož komprimovanú verziu
            compressed_file = history_file.parent / f"{history_file.stem}_COMPRESSED.md"

            # Pridaj header
            output = f"""# KOMPRIMOVANÁ HISTÓRIA CHATU - nex-automat

**Pôvodný súbor:** {history_file.name}
**Komprimované:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Pôvodná veľkosť:** {history_length:,} znakov
**Komprimovaná veľkosť:** {compressed_length:,} znakov
**Kompresia:** {compression_ratio:.1f}%

---

{compressed}

---

*Komprimované pomocou Claude Sonnet 4*
"""

            compressed_file.write_text(output, encoding="utf-8")
            print(f"💾 Uložené: {compressed_file}")

            return compressed

        except Exception as e:
            print(f"❌ Chyba pri kompresii: {e}")
            raise

    def compress_session_notes(self):
        """Skomprimuj aktuálne session notes"""
        notes_file = self.session_notes_dir / "SESSION_NOTES.md"

        if not notes_file.exists():
            print(f"❌ Session notes neexistujú: {notes_file}")
            return None

        return self.compress_chat_history(notes_file)

    def compress_init_prompt(self):
        """Skomprimuj init prompt"""
        init_file = self.session_notes_dir / "INIT_PROMPT_NEW_CHAT.md"

        if not init_file.exists():
            print(f"❌ Init prompt neexistuje: {init_file}")
            return None

        return self.compress_chat_history(init_file)

    def batch_compress(self, directory: Path):
        """Skomprimuj všetky .md súbory v adresári"""
        if not directory.exists():
            print(f"❌ Adresár neexistuje: {directory}")
            return

        md_files = list(directory.glob("*.md"))

        if not md_files:
            print(f"⚠️ Žiadne .md súbory v: {directory}")
            return

        print(f"\n{'=' * 60}")
        print(f"📦 BATCH KOMPRESIA (nex-automat) - {len(md_files)} súborov")
        print("=" * 60)

        success_count = 0
        total_original = 0
        total_compressed = 0

        for md_file in md_files:
            # Preskočíme už komprimované súbory
            if "_COMPRESSED" in md_file.stem:
                continue

            try:
                original_size = len(md_file.read_text(encoding="utf-8"))
                compressed = self.compress_chat_history(md_file)
                compressed_size = len(compressed)

                total_original += original_size
                total_compressed += compressed_size
                success_count += 1

                print()  # Prázdny riadok medzi súbormi

            except Exception as e:
                print(f"❌ Chyba pri {md_file.name}: {e}\n")

        # Celková štatistika
        if success_count > 0:
            total_ratio = (1 - total_compressed / total_original) * 100
            print("=" * 60)
            print(f"✅ Komprimovaných: {success_count}/{len(md_files)}")
            print(f"📊 Celková kompresia: {total_ratio:.1f}%")
            print("=" * 60)


def main():
    """Hlavná funkcia"""
    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "":
        print("\n❌ CHYBA: ANTHROPIC_API_KEY nie je nastavený")
        print("\nAby si mohol použiť Context Compressor, musíš:")
        print("1. Otvoriť: tools/config.py")
        print("2. Nastaviť: ANTHROPIC_API_KEY = 'sk-ant-...'")
        print("3. Získaj API key na: https://console.anthropic.com/\n")
        return

    compressor = ContextCompressor()

    if len(sys.argv) < 2:
        print("\nContext Compressor (nex-automat) - Použitie:")
        print("  python context-compressor.py notes     - Komprimuj session notes")
        print("  python context-compressor.py init      - Komprimuj init prompt")
        print("  python context-compressor.py file <path> - Komprimuj konkrétny súbor")
        print("  python context-compressor.py batch <dir> - Komprimuj všetky .md v adresári")
        print()
        return

    command = sys.argv[1].lower()

    try:
        if command == "notes":
            compressor.compress_session_notes()

        elif command == "init":
            compressor.compress_init_prompt()

        elif command == "file" and len(sys.argv) > 2:
            file_path = Path(sys.argv[2])
            compressor.compress_chat_history(file_path)

        elif command == "batch" and len(sys.argv) > 2:
            dir_path = Path(sys.argv[2])
            compressor.batch_compress(dir_path)

        else:
            print("❌ Neznámy príkaz alebo chýbajúce parametre")

    except Exception as e:
        print(f"\n❌ CHYBA: {e}\n")


if __name__ == "__main__":
    main()
