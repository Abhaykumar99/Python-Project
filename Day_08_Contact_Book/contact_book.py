# Contact Book 📒
# Concepts: Dictionaries, File I/O, JSON, Functions, Search & Sort

import json
import os


DATA_FILE = os.path.join(os.path.dirname(__file__), "contacts.json")


def load_contacts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_contacts(contacts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4)


def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║        📒  CONTACT  BOOK  📒           ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_menu(contacts):
    total = len(contacts)
    print(f"  ┌─────────────────────────────────────────┐")
    print(f"  │   Contacts saved: {total:<23}│")
    print(f"  ├─────────────────────────────────────────┤")
    print(f"  │   1  ➜  Add Contact                     │")
    print(f"  │   2  ➜  View All Contacts               │")
    print(f"  │   3  ➜  Search Contact                  │")
    print(f"  │   4  ➜  Edit Contact                    │")
    print(f"  │   5  ➜  Delete Contact                  │")
    print(f"  │   6  ➜  Exit                            │")
    print(f"  └─────────────────────────────────────────┘")


def add_contact(contacts):
    print("\n  ── Add New Contact ──────────────────────")
    name = input("  👤  Full Name   : ").strip().title()
    if not name:
        print("  ⚠️  Name cannot be empty.\n")
        return

    if name in contacts:
        print(f"  ⚠️  '{name}' already exists. Use Edit to update.\n")
        return

    phone  = input("  📞  Phone       : ").strip()
    email  = input("  📧  Email       : ").strip()
    city   = input("  🏙️  City        : ").strip()

    contacts[name] = {"phone": phone, "email": email, "city": city}
    save_contacts(contacts)
    print(f"\n  ✅  Contact '{name}' added successfully!\n")


def view_all(contacts):
    print()
    if not contacts:
        print("  📭  No contacts yet. Add some!\n")
        return

    sorted_contacts = sorted(contacts.items())
    print(f"  ── All Contacts ({len(contacts)}) ───────────────────")
    print(f"  {'#':<4} {'Name':<22} {'Phone':<16} {'City'}")
    print(f"  {'─'*4} {'─'*22} {'─'*16} {'─'*14}")

    for i, (name, info) in enumerate(sorted_contacts, 1):
        phone = info.get("phone", "—") or "—"
        city  = info.get("city",  "—") or "—"
        print(f"  {i:<4} {name:<22} {phone:<16} {city}")
    print()


def search_contact(contacts):
    print("\n  ── Search Contact ───────────────────────")
    query = input("  🔍  Enter name to search: ").strip().lower()
    if not query:
        print("  ⚠️  Search query cannot be empty.\n")
        return

    results = {n: d for n, d in contacts.items() if query in n.lower()}

    if not results:
        print(f"  ❌  No contacts found for '{query}'.\n")
        return

    print(f"\n  ✅  Found {len(results)} result(s):\n")
    for name, info in results.items():
        _print_contact(name, info)


def edit_contact(contacts):
    print("\n  ── Edit Contact ─────────────────────────")
    view_all(contacts)
    if not contacts:
        return

    name = input("  ✏️  Enter exact name to edit: ").strip().title()
    if name not in contacts:
        print(f"  ❌  '{name}' not found.\n")
        return

    info = contacts[name]
    print(f"\n  Editing: {name}")
    print("  (Press Enter to keep current value)\n")

    new_phone = input(f"  📞  Phone [{info.get('phone','')}]: ").strip()
    new_email = input(f"  📧  Email [{info.get('email','')}]: ").strip()
    new_city  = input(f"  🏙️  City  [{info.get('city', '')}]: ").strip()

    if new_phone: contacts[name]["phone"] = new_phone
    if new_email: contacts[name]["email"] = new_email
    if new_city:  contacts[name]["city"]  = new_city

    save_contacts(contacts)
    print(f"\n  ✅  '{name}' updated successfully!\n")


def delete_contact(contacts):
    print("\n  ── Delete Contact ───────────────────────")
    view_all(contacts)
    if not contacts:
        return

    name = input("  🗑️  Enter exact name to delete: ").strip().title()
    if name not in contacts:
        print(f"  ❌  '{name}' not found.\n")
        return

    confirm = input(f"  ⚠️  Delete '{name}'? (yes/no): ").strip().lower()
    if confirm in ("yes", "y"):
        del contacts[name]
        save_contacts(contacts)
        print(f"  ✅  '{name}' deleted.\n")
    else:
        print("  ↩️  Cancelled.\n")


def _print_contact(name, info):
    print(f"  ┌─────────────────────────────────────┐")
    print(f"  │  👤  {name}")
    print(f"  │  📞  {info.get('phone', '—') or '—'}")
    print(f"  │  📧  {info.get('email', '—') or '—'}")
    print(f"  │  🏙️  {info.get('city',  '—') or '—'}")
    print(f"  └─────────────────────────────────────┘")
    print()


def main():
    show_banner()
    contacts = load_contacts()
    print(f"  📂  Loaded {len(contacts)} contact(s) from storage.\n")

    while True:
        show_menu(contacts)
        choice = input("\n  👉  Select an option (1-6): ").strip()

        if   choice == "1": add_contact(contacts)
        elif choice == "2": view_all(contacts)
        elif choice == "3": search_contact(contacts)
        elif choice == "4": edit_contact(contacts)
        elif choice == "5": delete_contact(contacts)
        elif choice == "6":
            print("\n  ════════════════════════════════════════")
            print(f"  📒  {len(contacts)} contact(s) saved. Goodbye! 👋\n")
            break
        else:
            print("\n  ⚠️  Invalid option! Please select 1 to 6.\n")


if __name__ == "__main__":
    main()
