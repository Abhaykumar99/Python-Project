# Expense Tracker 💸
# Concepts: CSV File I/O, datetime, Lists of Dicts, Functions, Aggregation

import csv
import os
from datetime import datetime


DATA_FILE = os.path.join(os.path.dirname(__file__), "expenses.csv")
FIELDNAMES = ["date", "category", "description", "amount"]

CATEGORIES = {
    "1": "🍔 Food",
    "2": "🚗 Transport",
    "3": "🎮 Entertainment",
    "4": "🛒 Shopping",
    "5": "💊 Health",
    "6": "📚 Education",
    "7": "🏠 Rent/Bills",
    "8": "📦 Other",
}


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║       💸  EXPENSE  TRACKER  💸         ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_menu():
    print("  ┌────────────────────────────────────────┐")
    print("  │              MAIN MENU                  │")
    print("  ├────────────────────────────────────────┤")
    print("  │   1  ➜  Add Expense                     │")
    print("  │   2  ➜  View All Expenses               │")
    print("  │   3  ➜  Monthly Summary                 │")
    print("  │   4  ➜  Category Summary                │")
    print("  │   5  ➜  Delete Last Expense             │")
    print("  │   6  ➜  Exit                            │")
    print("  └────────────────────────────────────────┘")


def load_expenses():
    expenses = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["amount"] = float(row["amount"])
                expenses.append(row)
    return expenses


def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(expenses)


def pick_category():
    print()
    print("  ── Pick a Category ──────────────────────")
    for key, label in CATEGORIES.items():
        print(f"    {key})  {label}")
    print()
    while True:
        choice = input("  👉  Category (1-8): ").strip()
        if choice in CATEGORIES:
            return CATEGORIES[choice]
        print("  ⚠️  Enter 1 to 8.")


def add_expense(expenses):
    print("\n  ── Add Expense ──────────────────────────")

    # Amount
    while True:
        try:
            amount = float(input("  💰  Amount (₹): ").strip())
            if amount <= 0:
                print("  ⚠️  Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("  ⚠️  Enter a valid number.")

    category = pick_category()
    desc = input("  📝  Description (optional): ").strip() or "—"
    date = datetime.now().strftime("%Y-%m-%d")

    expenses.append({"date": date, "category": category, "description": desc, "amount": amount})
    save_expenses(expenses)
    print(f"\n  ✅  Expense added: {category}  ₹{amount:.2f}  on {date}\n")


def view_all(expenses):
    print()
    if not expenses:
        print("  📭  No expenses recorded yet.\n")
        return

    print(f"  ── All Expenses ({len(expenses)}) ──────────────────────")
    print(f"  {'#':<4} {'Date':<12} {'Category':<22} {'Amount':>9}  Description")
    print(f"  {'─'*4} {'─'*12} {'─'*22} {'─'*9}  {'─'*20}")

    total = 0
    for i, e in enumerate(expenses, 1):
        cat = e["category"].split()[-1]   # strip emoji for width
        print(f"  {i:<4} {e['date']:<12} {e['category']:<22} ₹{e['amount']:>8.2f}  {e['description'][:20]}")
        total += e["amount"]

    print(f"  {'─'*60}")
    print(f"  {'TOTAL':>40}  ₹{total:>8.2f}")
    print()


def monthly_summary(expenses):
    print()
    if not expenses:
        print("  📭  No expenses recorded yet.\n")
        return

    monthly = {}
    for e in expenses:
        month = e["date"][:7]   # YYYY-MM
        monthly[month] = monthly.get(month, 0) + e["amount"]

    print(f"  ── Monthly Summary ──────────────────────")
    print(f"  {'Month':<12}  {'Total':>10}")
    print(f"  {'─'*12}  {'─'*10}")

    grand_total = 0
    for month in sorted(monthly):
        label = datetime.strptime(month, "%Y-%m").strftime("%b %Y")
        print(f"  {label:<12}  ₹{monthly[month]:>9.2f}")
        grand_total += monthly[month]

    print(f"  {'─'*24}")
    print(f"  {'Grand Total':<12}  ₹{grand_total:>9.2f}\n")


def category_summary(expenses):
    print()
    if not expenses:
        print("  📭  No expenses recorded yet.\n")
        return

    cat_totals = {}
    for e in expenses:
        cat = e["category"]
        cat_totals[cat] = cat_totals.get(cat, 0) + e["amount"]

    grand_total = sum(cat_totals.values())

    print(f"  ── Category Summary ─────────────────────")
    print(f"  {'Category':<24}  {'Amount':>10}  {'Share':>6}")
    print(f"  {'─'*24}  {'─'*10}  {'─'*6}")

    for cat, total in sorted(cat_totals.items(), key=lambda x: -x[1]):
        pct = (total / grand_total) * 100
        bar = "█" * int(pct / 5)
        print(f"  {cat:<24}  ₹{total:>9.2f}  {pct:>5.1f}%  {bar}")

    print(f"  {'─'*44}")
    print(f"  {'TOTAL':<24}  ₹{grand_total:>9.2f}\n")


def delete_last(expenses):
    if not expenses:
        print("\n  📭  No expenses to delete.\n")
        return

    last = expenses[-1]
    print(f"\n  Last entry: {last['date']}  {last['category']}  ₹{last['amount']:.2f}  {last['description']}")
    confirm = input("  ⚠️  Delete this entry? (yes/no): ").strip().lower()
    if confirm in ("yes", "y"):
        expenses.pop()
        save_expenses(expenses)
        print("  ✅  Last expense deleted.\n")
    else:
        print("  ↩️  Cancelled.\n")


def main():
    show_banner()
    expenses = load_expenses()
    print(f"  📂  Loaded {len(expenses)} expense(s) from storage.\n")

    while True:
        show_menu()
        choice = input("\n  👉  Select an option (1-6): ").strip()

        if   choice == "1": add_expense(expenses)
        elif choice == "2": view_all(expenses)
        elif choice == "3": monthly_summary(expenses)
        elif choice == "4": category_summary(expenses)
        elif choice == "5": delete_last(expenses)
        elif choice == "6":
            total = sum(e["amount"] for e in expenses)
            print(f"\n  ════════════════════════════════════════")
            print(f"  💸  Total tracked: ₹{total:.2f}  |  {len(expenses)} expense(s).")
            print(f"  👋  Goodbye!\n")
            break
        else:
            print("\n  ⚠️  Invalid option! Please select 1 to 6.\n")


if __name__ == "__main__":
    main()
