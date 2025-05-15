# Password Generator 🔐
# Concepts: String Module, Random, Lists, Functions, User Options

import random
import string


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║       🔐  PASSWORD GENERATOR  🔐       ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_menu():
    print("  ┌────────────────────────────────────────┐")
    print("  │              MAIN MENU                  │")
    print("  ├────────────────────────────────────────┤")
    print("  │   1  ➜  Quick Generate (by strength)   │")
    print("  │   2  ➜  Custom Generate                 │")
    print("  │   3  ➜  Exit                            │")
    print("  └────────────────────────────────────────┘")


def get_strength_settings():
    print()
    print("  ┌────────────────────────────────────────┐")
    print("  │       Select Password Strength:         │")
    print("  ├────────────────────────────────────────┤")
    print("  │   1  ➜  Weak     (letters only, 8)     │")
    print("  │   2  ➜  Medium   (letters+digits, 12)  │")
    print("  │   3  ➜  Strong   (all chars, 16)       │")
    print("  │   4  ➜  Ultra    (all chars, 24)       │")
    print("  └────────────────────────────────────────┘")

    presets = {
        "1": ("Weak",   8,  True,  False, False),
        "2": ("Medium", 12, True,  True,  False),
        "3": ("Strong", 16, True,  True,  True),
        "4": ("Ultra",  24, True,  True,  True),
    }

    while True:
        choice = input("\n  👉  Select strength (1-4): ").strip()
        if choice in presets:
            return presets[choice]
        print("  ⚠️  Please enter 1 to 4.")


def get_custom_settings():
    print()
    # Length
    while True:
        try:
            length = int(input("  📏  Password length (4-128): ").strip())
            if 4 <= length <= 128:
                break
            print("  ⚠️  Enter a length between 4 and 128.")
        except ValueError:
            print("  ⚠️  Please enter a valid number.")

    def yes_no(prompt):
        while True:
            ans = input(f"  {prompt} (y/n): ").strip().lower()
            if ans in ("y", "yes"):
                return True
            if ans in ("n", "no"):
                return False
            print("  ⚠️  Enter y or n.")

    use_letters  = yes_no("🔤  Include letters?")
    use_digits   = yes_no("🔢  Include digits?")
    use_symbols  = yes_no("🔣  Include symbols?")

    if not (use_letters or use_digits or use_symbols):
        print("  ⚠️  At least one character type must be selected. Defaulting to letters.")
        use_letters = True

    return ("Custom", length, use_letters, use_digits, use_symbols)


def build_charset(use_letters, use_digits, use_symbols):
    charset = ""
    guaranteed = []

    if use_letters:
        charset += string.ascii_letters
        guaranteed.append(random.choice(string.ascii_lowercase))
        guaranteed.append(random.choice(string.ascii_uppercase))
    if use_digits:
        charset += string.digits
        guaranteed.append(random.choice(string.digits))
    if use_symbols:
        charset += string.punctuation
        guaranteed.append(random.choice(string.punctuation))

    return charset, guaranteed


def generate_password(length, use_letters, use_digits, use_symbols):
    charset, guaranteed = build_charset(use_letters, use_digits, use_symbols)

    # Fill remaining length with random chars from charset
    remaining = length - len(guaranteed)
    rest = [random.choice(charset) for _ in range(remaining)]

    # Shuffle guaranteed + rest together
    password_list = guaranteed + rest
    random.shuffle(password_list)
    return "".join(password_list)


def rate_password(password):
    length = len(password)
    has_lower   = any(c.islower() for c in password)
    has_upper   = any(c.isupper() for c in password)
    has_digit   = any(c.isdigit() for c in password)
    has_symbol  = any(c in string.punctuation for c in password)

    score = sum([has_lower, has_upper, has_digit, has_symbol])

    if length >= 20 and score == 4:
        return ("🟢 ULTRA STRONG", 4)
    elif length >= 14 and score >= 3:
        return ("🟡 STRONG", 3)
    elif length >= 10 and score >= 2:
        return ("🟠 MEDIUM", 2)
    else:
        return ("🔴 WEAK", 1)


def display_password(label, password):
    rating, _ = rate_password(password)
    print()
    print("  ┌────────────────────────────────────────────────┐")
    print(f"  │  🔑  {label} Password ({len(password)} chars)")
    print("  ├────────────────────────────────────────────────┤")
    print(f"  │  {password}")
    print("  ├────────────────────────────────────────────────┤")
    print(f"  │  Strength: {rating}")
    print("  └────────────────────────────────────────────────┘")
    print()


def quick_generate():
    label, length, use_letters, use_digits, use_symbols = get_strength_settings()

    while True:
        password = generate_password(length, use_letters, use_digits, use_symbols)
        display_password(label, password)

        again = input("  [Enter] ➜ Regenerate  |  [q] ➜ Back to Menu\n  👉  ").strip().lower()
        if again == "q":
            break
        print()


def custom_generate():
    label, length, use_letters, use_digits, use_symbols = get_custom_settings()
    print()

    while True:
        password = generate_password(length, use_letters, use_digits, use_symbols)
        display_password(label, password)

        again = input("  [Enter] ➜ Regenerate  |  [q] ➜ Back to Menu\n  👉  ").strip().lower()
        if again == "q":
            break
        print()


def main():
    show_banner()

    while True:
        show_menu()
        choice = input("\n  👉  Select an option (1-3): ").strip()

        if choice == "1":
            quick_generate()
        elif choice == "2":
            custom_generate()
        elif choice == "3":
            print("\n  ════════════════════════════════════════")
            print("  🔐  Stay safe! Use strong passwords.")
            print("  👋  Goodbye!\n")
            break
        else:
            print("\n  ⚠️  Invalid option! Please select 1 to 3.\n")


if __name__ == "__main__":
    main()
