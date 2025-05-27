# Number to Words Converter 🔢➡️🔤
# Concepts: Recursion, Nested Conditions, Large Numbers, Indian & International Systems

ONES = [
    "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
    "Sixteen", "Seventeen", "Eighteen", "Nineteen"
]

TENS = [
    "", "", "Twenty", "Thirty", "Forty", "Fifty",
    "Sixty", "Seventy", "Eighty", "Ninety"
]

# International scale
INTL_SCALE = [
    (10**12, "Trillion"),
    (10**9,  "Billion"),
    (10**6,  "Million"),
    (10**3,  "Thousand"),
    (10**2,  "Hundred"),
]

# Indian scale
INDIAN_SCALE = [
    (10**12, "Lakh Crore"),
    (10**7,  "Crore"),
    (10**5,  "Lakh"),
    (10**3,  "Thousand"),
    (10**2,  "Hundred"),
]


def three_digits_to_words(n):
    """Convert a 3-digit number (0–999) to words."""
    if n == 0:
        return ""
    elif n < 20:
        return ONES[n]
    elif n < 100:
        rest = ONES[n % 10]
        return TENS[n // 10] + (" " + rest if rest else "")
    else:
        rest = three_digits_to_words(n % 100)
        return ONES[n // 100] + " Hundred" + (" " + rest if rest else "")


def to_words_international(n):
    """Convert integer n to English words (international: million, billion...)."""
    if n < 0:
        return "Negative " + to_words_international(-n)
    if n == 0:
        return "Zero"

    parts = []
    for value, name in INTL_SCALE:
        if n >= value:
            chunk = n // value
            parts.append(three_digits_to_words(chunk) + " " + name)
            n %= value

    if n > 0:
        parts.append(three_digits_to_words(n))

    return " ".join(parts)


def to_words_indian(n):
    """Convert integer n to Indian system words (Lakh, Crore...)."""
    if n < 0:
        return "Negative " + to_words_indian(-n)
    if n == 0:
        return "Zero"

    parts = []
    for value, name in INDIAN_SCALE:
        if n >= value:
            chunk = n // value
            parts.append(three_digits_to_words(chunk) + " " + name)
            n %= value

    if n > 0:
        parts.append(three_digits_to_words(n))

    return " ".join(parts)


def format_indian(n):
    """Format number with Indian commas: 1,00,000."""
    s = str(abs(n))
    if len(s) <= 3:
        return ("-" if n < 0 else "") + s
    result = s[-3:]
    s = s[:-3]
    while s:
        result = s[-2:] + "," + result
        s = s[:-2]
    return ("-" if n < 0 else "") + result.lstrip(",")


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║   🔢  NUMBER TO WORDS CONVERTER  🔤    ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_menu():
    print("  ┌────────────────────────────────────────┐")
    print("  │              MAIN MENU                  │")
    print("  ├────────────────────────────────────────┤")
    print("  │   1  ➜  Number → Words (International) │")
    print("  │   2  ➜  Number → Words (Indian System) │")
    print("  │   3  ➜  Both Systems Side by Side       │")
    print("  │   4  ➜  Exit                            │")
    print("  └────────────────────────────────────────┘")


def get_number():
    while True:
        raw = input("\n  🔢  Enter a number: ").strip().replace(",", "")
        try:
            n = int(raw)
            if abs(n) > 10**15:
                print("  ⚠️  Number too large (max: 10^15).")
                continue
            return n
        except ValueError:
            print("  ⚠️  Enter a valid whole number (decimals not supported).")


def show_result(n, system, words):
    intl_fmt   = f"{n:,}"
    indian_fmt = format_indian(n)
    print()
    print("  ┌────────────────────────────────────────────────────┐")
    print(f"  │  Number ({system})")
    print(f"  │  Intl   : {intl_fmt}")
    print(f"  │  Indian : {indian_fmt}")
    print(f"  ├────────────────────────────────────────────────────┤")
    # Word-wrap at ~52 chars
    words_lines = []
    line = "  │  "
    for word in words.split():
        if len(line) + len(word) + 1 > 54:
            words_lines.append(line)
            line = "  │    " + word
        else:
            line += word + " "
    words_lines.append(line)
    for wl in words_lines:
        print(wl)
    print("  └────────────────────────────────────────────────────┘")
    print()


def main():
    show_banner()

    while True:
        show_menu()
        choice = input("\n  👉  Select (1-4): ").strip()

        if choice == "1":
            n = get_number()
            words = to_words_international(n)
            show_result(n, "International", words)

        elif choice == "2":
            n = get_number()
            words = to_words_indian(n)
            show_result(n, "Indian", words)

        elif choice == "3":
            n = get_number()
            intl   = to_words_international(n)
            indian = to_words_indian(n)
            print()
            print(f"  Number   : {n:,}")
            print(f"  Indian # : {format_indian(n)}")
            print()
            print(f"  International :")
            print(f"    {intl}")
            print()
            print(f"  Indian System :")
            print(f"    {indian}")
            print()

        elif choice == "4":
            print("\n  ════════════════════════════════════════")
            print("  🔢  Goodbye! Numbers are beautiful! 👋\n")
            break
        else:
            print("\n  ⚠️  Invalid option! Select 1 to 4.\n")


if __name__ == "__main__":
    main()
