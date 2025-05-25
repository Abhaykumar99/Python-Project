# Morse Code Translator 📡
# Concepts: Dictionaries, String methods, Bidirectional lookup, File I/O

import os

MORSE_CODE = {
    'A': '.-',   'B': '-...', 'C': '-.-.',  'D': '-..',
    'E': '.',    'F': '..-.', 'G': '--.',   'H': '....',
    'I': '..',   'J': '.---', 'K': '-.-',   'L': '.-..',
    'M': '--',   'N': '-.',   'O': '---',   'P': '.--.',
    'Q': '--.-', 'R': '.-.',  'S': '...',   'T': '-',
    'U': '..-',  'V': '...-', 'W': '.--',   'X': '-..-',
    'Y': '-.--', 'Z': '--..',

    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',

    '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--',
    "'": '.----.', '(': '-.--.',  ')': '-.--.-', '&': '.-...',
    ':': '---...', ';': '-.-.-.', '/': '-..-.',  '-': '-....-',
    '_': '..--.-', '"': '.-..-.', '$': '...-..-','@': '.--.-.',
    '+': '.-.-.',  '=': '-...-',
}

# Reverse map: morse → letter
REVERSE_MORSE = {v: k for k, v in MORSE_CODE.items()}

WORD_SEP    = "  "   # double space separates words in morse
LETTER_SEP  = " "    # single space separates letters


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║    📡  MORSE CODE TRANSLATOR  📡       ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_menu():
    print("  ┌────────────────────────────────────────┐")
    print("  │              MAIN MENU                  │")
    print("  ├────────────────────────────────────────┤")
    print("  │   1  ➜  Text   → Morse Code            │")
    print("  │   2  ➜  Morse  → Text                  │")
    print("  │   3  ➜  Show Morse Code Table           │")
    print("  │   4  ➜  Save Result to File             │")
    print("  │   5  ➜  Exit                            │")
    print("  └────────────────────────────────────────┘")


def text_to_morse(text):
    words = text.upper().split()
    morse_words = []
    unknown = []
    for word in words:
        letters = []
        for ch in word:
            if ch in MORSE_CODE:
                letters.append(MORSE_CODE[ch])
            else:
                letters.append("?")
                if ch not in unknown:
                    unknown.append(ch)
        morse_words.append(LETTER_SEP.join(letters))
    return WORD_SEP.join(morse_words), unknown


def morse_to_text(morse):
    words = morse.strip().split("   ")      # 3 spaces = word boundary
    result = []
    unknown = []
    for word in words:
        letters = word.split()
        chars = []
        for code in letters:
            if code in REVERSE_MORSE:
                chars.append(REVERSE_MORSE[code])
            else:
                chars.append("?")
                if code not in unknown:
                    unknown.append(code)
        result.append("".join(chars))
    return " ".join(result), unknown


def show_morse_table():
    print()
    print("  ── Morse Code Reference Table ────────────")
    print()

    # Letters
    print("  LETTERS:")
    letters = [(k, v) for k, v in MORSE_CODE.items() if k.isalpha()]
    for i, (ch, code) in enumerate(letters):
        end = "\n" if (i + 1) % 4 == 0 else ""
        print(f"   {ch} : {code:<8}", end=end)
    print("\n")

    # Digits
    print("  DIGITS:")
    digits = [(k, v) for k, v in MORSE_CODE.items() if k.isdigit()]
    for i, (ch, code) in enumerate(digits):
        print(f"   {ch} : {code:<8}", end="\n" if (i + 1) % 5 == 0 else "")
    print("\n")

    # Punctuation
    print("  PUNCTUATION:")
    puncts = [(k, v) for k, v in MORSE_CODE.items() if not k.isalnum()]
    for i, (ch, code) in enumerate(puncts):
        print(f"   {ch} : {code:<10}", end="\n" if (i + 1) % 4 == 0 else "")
    print("\n")

    print("  NOTE: Letters separated by SPACE, words by 3 SPACES")
    print()


def save_to_file(original, result, direction):
    filename = f"morse_output.txt"
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{direction}]\n")
        f.write(f"Input : {original}\n")
        f.write(f"Output: {result}\n")
        f.write("-" * 50 + "\n")
    return path


def main():
    show_banner()
    last_result = None
    last_input  = None
    last_dir    = None

    while True:
        show_menu()
        choice = input("\n  👉  Select (1-5): ").strip()

        if choice == "1":
            text = input("\n  📝  Enter text: ").strip()
            if not text:
                print("  ⚠️  Nothing entered.\n")
                continue
            result, unknown = text_to_morse(text)
            print(f"\n  ── Morse Code ──────────────────────────")
            print(f"  {result}")
            if unknown:
                print(f"\n  ⚠️  Unsupported characters skipped: {', '.join(unknown)}")
            print()
            last_input, last_result, last_dir = text, result, "Text → Morse"

        elif choice == "2":
            print("\n  📡  Enter Morse code:")
            print("  (Use SPACE between letters, 3 SPACES between words)")
            morse = input("  > ").strip()
            if not morse:
                print("  ⚠️  Nothing entered.\n")
                continue
            result, unknown = morse_to_text(morse)
            print(f"\n  ── Decoded Text ────────────────────────")
            print(f"  {result}")
            if unknown:
                print(f"\n  ⚠️  Unknown codes: {', '.join(unknown)}")
            print()
            last_input, last_result, last_dir = morse, result, "Morse → Text"

        elif choice == "3":
            show_morse_table()

        elif choice == "4":
            if last_result is None:
                print("\n  ⚠️  Nothing to save yet. Translate something first.\n")
                continue
            path = save_to_file(last_input, last_result, last_dir)
            print(f"\n  ✅  Saved to: {path}\n")

        elif choice == "5":
            print("\n  ════════════════════════════════════════")
            print("  📡  Goodbye! -- --- .-. ... . 👋\n")
            break
        else:
            print("\n  ⚠️  Invalid option! Select 1 to 5.\n")


if __name__ == "__main__":
    main()
