# Calculator App

import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_num(num):
    if isinstance(num, str):
        return num
    return int(num) if num == int(num) else round(num, 6)


def get_numbers():
    while True:
        try:
            count = int(input("  Enter how many numbers: "))
            if count < 2:
                print("  ⚠️  Minimum 2 numbers required!\n")
                continue
            break
        except ValueError:
            print("  ⚠️  Please enter a valid number!\n")

    numbers = []
    for i in range(1, count + 1):
        while True:
            try:
                n = float(input(f"  Number {i}: "))
                numbers.append(n)
                break
            except ValueError:
                print("  ⚠️  Invalid input! Try again.\n")

    return numbers


def calculate(numbers, symbol):
    result = numbers[0]
    expression_parts = [str(format_num(numbers[0]))]

    for i in range(1, len(numbers)):
        n = numbers[i]
        expression_parts.append(f" {symbol} {format_num(n)}")

        if symbol == "+":
            result += n
        elif symbol == "−":
            result -= n
        elif symbol == "×":
            result *= n
        elif symbol == "÷":
            if n == 0:
                return "".join(expression_parts), "❌ Error: Cannot divide by zero!"
            result /= n

    expression = "".join(expression_parts)
    return expression, format_num(result)


def show_banner():
    clear_screen()
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║        🧮  PYTHON CALCULATOR  🧮      ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_menu():
    print("  ┌────────────────────────────────────────┐")
    print("  │         Select an Operation:            │")
    print("  ├────────────────────────────────────────┤")
    print("  │   1  ➜  Addition          ( + )        │")
    print("  │   2  ➜  Subtraction       ( − )        │")
    print("  │   3  ➜  Multiplication    ( × )        │")
    print("  │   4  ➜  Division          ( ÷ )        │")
    print("  │   5  ➜  History           ( 📜 )       │")
    print("  │   6  ➜  Exit              ( 👋 )       │")
    print("  └────────────────────────────────────────┘")


def show_history(history):
    if not history:
        print("\n  📜 No calculations yet!\n")
        return

    print("\n  ╔════════════════════════════════════════╗")
    print("  ║         📜 CALCULATION HISTORY          ║")
    print("  ╠════════════════════════════════════════╣")

    for i, record in enumerate(history, 1):
        print(f"  ║  {i}. {record}")

    print("  ╚════════════════════════════════════════╝\n")


def main():
    show_banner()

    operations = {
        "1": ("Addition", "+"),
        "2": ("Subtraction", "−"),
        "3": ("Multiplication", "×"),
        "4": ("Division", "÷"),
    }

    history = []
    total_calculations = 0

    while True:
        show_menu()
        choice = input("\n  👉 Enter your choice (1-6): ").strip()

        if choice == "6":
            print("\n  ════════════════════════════════════════")
            print(f"  👋 Goodbye! Total {total_calculations} calculation(s) done.")
            if history:
                print(f"  📜 Last: {history[-1]}")
            print("  ════════════════════════════════════════\n")
            break

        if choice == "5":
            show_history(history)
            input("  Press Enter to go back...")
            show_banner()
            continue

        if choice not in operations:
            print("\n  ⚠️  Invalid choice! Please select 1 to 6.\n")
            continue

        name, symbol = operations[choice]

        print(f"\n  ━━━ {name} ━━━")
        print("  (You can enter any number of values)\n")

        numbers = get_numbers()
        expression, result = calculate(numbers, symbol)

        print("\n  ┌──────────────────────────────────────────┐")
        print(f"  │  ✅ {expression} = {result}")
        print("  └──────────────────────────────────────────┘")

        history.append(f"{expression} = {result}")
        total_calculations += 1

        print("\n  [Enter] ➜ Continue  |  [q] ➜ Exit")
        again = input("  👉 ").strip().lower()

        if again == "q":
            print("\n  ════════════════════════════════════════")
            print(f"  👋 Goodbye! Total {total_calculations} calculation(s) done.")
            print("  ════════════════════════════════════════\n")
            break

        show_banner()


if __name__ == "__main__":
    main()
