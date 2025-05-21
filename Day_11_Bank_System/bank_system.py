# Bank Account System 🏦
# Concepts: Classes (OOP), Objects, Methods, JSON persistence, datetime

import json
import os
import random
from datetime import datetime


DATA_FILE = os.path.join(os.path.dirname(__file__), "bank_data.json")


def generate_acc_number():
    date_part = datetime.now().strftime("%Y%m%d")
    rand_part = random.randint(1000, 9999)
    return f"ACC-{date_part}-{rand_part}"


class BankAccount:
    def __init__(self, owner, balance=0.0, transactions=None, acc_number=None, pin=None):
        self.owner        = owner
        self.balance      = balance
        self.transactions = transactions or []
        self.acc_number   = acc_number or generate_acc_number()
        self.pin          = pin  # stored as plain string (4 digits)

    def set_pin(self, pin):
        self.pin = pin

    def verify_pin(self, pin):
        return self.pin == pin

    # ── Core operations ───────────────────────────────────────
    def deposit(self, amount):
        if amount <= 0:
            return False, "Amount must be greater than ₹0."
        self.balance += amount
        self._log("DEPOSIT", amount)
        return True, f"₹{amount:.2f} deposited. New balance: ₹{self.balance:.2f}"

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Amount must be greater than ₹0."
        if amount > self.balance:
            return False, f"Insufficient funds! Available: ₹{self.balance:.2f}"
        self.balance -= amount
        self._log("WITHDRAW", amount)
        return True, f"₹{amount:.2f} withdrawn. New balance: ₹{self.balance:.2f}"

    def get_balance(self):
        return self.balance

    def get_statement(self):
        return self.transactions

    # ── Internal ──────────────────────────────────────────────
    def _log(self, txn_type, amount):
        self.transactions.append({
            "type":    txn_type,
            "amount":  amount,
            "balance": self.balance,
            "date":    datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

    # ── Serialization ─────────────────────────────────────────
    def to_dict(self):
        return {
            "owner":        self.owner,
            "acc_number":   self.acc_number,
            "pin":          self.pin,
            "balance":      self.balance,
            "transactions": self.transactions,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["owner"], data["balance"], data["transactions"],
                   data.get("acc_number"), data.get("pin"))


# ── File helpers ──────────────────────────────────────────────
def load_accounts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
            # Key is acc_number
            return {acc_no: BankAccount.from_dict(d) for acc_no, d in raw.items()}
    return {}


def save_accounts(accounts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({acc_no: acc.to_dict() for acc_no, acc in accounts.items()}, f, indent=4)


# ── UI helpers ────────────────────────────────────────────────
def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║       🏦  BANK ACCOUNT SYSTEM  🏦      ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def get_pin(prompt="  🔒  Set 4-digit PIN: "):
    while True:
        pin = input(prompt).strip()
        if pin.isdigit() and len(pin) == 4:
            return pin
        print("  ⚠️  PIN must be exactly 4 digits (e.g. 1234).")


def ask_pin(prompt="  🔒  Enter PIN: "):
    """Ask PIN, mask input with * display."""
    return input(prompt).strip()


def get_amount(prompt):
    while True:
        try:
            val = float(input(prompt).strip())
            return val
        except ValueError:
            print("  ⚠️  Enter a valid number.\n")


def account_menu(account, accounts):
    while True:
        print(f"\n  ── Account: {account.owner} ──────────────────────")
        print(f"  �  Acc No : {account.acc_number}")
        print(f"  �💰  Balance: ₹{account.balance:,.2f}")
        print()
        print("  ┌────────────────────────────────────────┐")
        print("  │   1  ➜  Deposit                         │")
        print("  │   2  ➜  Withdraw                        │")
        print("  │   3  ➜  View Statement                  │")
        print("  │   4  ➜  Back to Main Menu               │")
        print("  └────────────────────────────────────────┘")

        choice = input("\n  👉  Select (1-4): ").strip()

        if choice == "1":
            amt = get_amount("  💵  Deposit amount (₹): ")
            ok, msg = account.deposit(amt)
            print(f"\n  {'✅' if ok else '❌'}  {msg}\n")
            save_accounts(accounts)

        elif choice == "2":
            amt = get_amount("  💸  Withdraw amount (₹): ")
            ok, msg = account.withdraw(amt)
            print(f"\n  {'✅' if ok else '❌'}  {msg}\n")
            save_accounts(accounts)

        elif choice == "3":
            txns = account.get_statement()
            print()
            if not txns:
                print("  📭  No transactions yet.\n")
            else:
                print(f"  ── Statement for {account.owner} ({len(txns)} transactions) ──")
                print(f"  {'#':<4} {'Date':<18} {'Type':<10} {'Amount':>10}  {'Balance':>12}")
                print(f"  {'─'*4} {'─'*18} {'─'*10} {'─'*10}  {'─'*12}")
                for i, t in enumerate(txns, 1):
                    sign = "+" if t["type"] == "DEPOSIT" else "-"
                    icon = "📥" if t["type"] == "DEPOSIT" else "📤"
                    print(f"  {i:<4} {t['date']:<18} {icon} {t['type']:<8} {sign}₹{t['amount']:>8.2f}  ₹{t['balance']:>10.2f}")
                print()

        elif choice == "4":
            break
        else:
            print("\n  ⚠️  Invalid option.\n")


def main():
    show_banner()
    accounts = load_accounts()
    print(f"  📂  {len(accounts)} account(s) loaded.\n")

    while True:
        print("  ┌────────────────────────────────────────┐")
        print("  │              MAIN MENU                  │")
        print("  ├────────────────────────────────────────┤")
        print("  │   1  ➜  Open New Account               │")
        print("  │   2  ➜  Login to Account               │")
        print("  │   3  ➜  List All Accounts              │")
        print("  │   4  ➜  Exit                           │")
        print("  └────────────────────────────────────────┘")
        choice = input("\n  👉  Select (1-4): ").strip()

        if choice == "1":
            name = input("\n  👤  Account holder name: ").strip().title()
            if not name:
                print("  ⚠️  Name cannot be empty.\n")
                continue
            pin = get_pin("  🔒  Set 4-digit PIN       : ")
            pin2 = get_pin("  🔒  Confirm PIN           : ")
            if pin != pin2:
                print("  ❌  PINs do not match. Try again.\n")
                continue
            opening = get_amount("  💰  Opening deposit (₹, or 0): ")
            acc = BankAccount(name, pin=pin)
            if opening > 0:
                acc.deposit(opening)
            accounts[acc.acc_number] = acc
            save_accounts(accounts)
            print(f"\n  ✅  Account created successfully!")
            print(f"  👤  Name      : {name}")
            print(f"  🔢  Acc Number: {acc.acc_number}")
            print(f"  �  PIN       : ****")
            print(f"  �💰  Balance   : ₹{acc.balance:,.2f}\n")

        elif choice == "2":
            if not accounts:
                print("\n  📭  No accounts yet. Create one first.\n")
                continue
            query = input("\n  👤  Enter account number (or name to list matches): ").strip()
            query_up = query.upper()
            query_lo = query.lower()

            # Exact account number match
            if query_up in accounts:
                account_menu(accounts[query_up], accounts)
                continue

            # Name search — may return multiple
            matches = [(no, a) for no, a in accounts.items() if query_lo in a.owner.lower()]
            if not matches:
                print(f"  ❌  No account found for '{query}'.\n")
            else:
                # Ask PIN — find matching account by PIN
                entered_pin = ask_pin("  🔒  Enter your PIN: ")
                pin_matches = [(no, a) for no, a in matches if a.verify_pin(entered_pin)]
                if not pin_matches:
                    print("  ❌  Wrong PIN! Access denied.\n")
                elif len(pin_matches) == 1:
                    print(f"  ✅  PIN verified. Welcome, {pin_matches[0][1].owner}!\n")
                    account_menu(pin_matches[0][1], accounts)
                else:
                    # Extremely rare: same name + same PIN → show acc number picker
                    print(f"  🔍  Multiple accounts with same PIN:")
                    for idx, (no, a) in enumerate(pin_matches, 1):
                        print(f"    {idx})  {a.owner}  |  {no}")
                    while True:
                        try:
                            sel = int(input("\n  👉  Select number: "))
                            if 1 <= sel <= len(pin_matches):
                                account_menu(pin_matches[sel - 1][1], accounts)
                                break
                            print(f"  ⚠️  Enter 1 to {len(pin_matches)}.")
                        except ValueError:
                            print("  ⚠️  Enter a valid number.")

        elif choice == "3":
            if not accounts:
                print("\n  📭  No accounts.\n")
                continue
            print(f"\n  ── All Accounts ({len(accounts)}) ──────────────────")
            print(f"  {'Name':<22}  {'Acc Number':<20}  {'Balance':>12}  Txns")
            print(f"  {'─'*22}  {'─'*20}  {'─'*12}  {'─'*4}")
            for acc_no, acc in sorted(accounts.items(), key=lambda x: x[1].owner):
                print(f"  {acc.owner:<22}  {acc_no:<20}  ₹{acc.balance:>10,.2f}  {len(acc.transactions):>4}")
            print()

        elif choice == "4":
            print("\n  ════════════════════════════════════════")
            print("  🏦  Thank you for banking with us! 👋\n")
            break
        else:
            print("\n  ⚠️  Invalid option!\n")


if __name__ == "__main__":
    main()
