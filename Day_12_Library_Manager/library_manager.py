# Library Management System 📚
# Concepts: OOP with Multiple Classes, Inheritance, JSON, Search & Filter

import json
import os
from datetime import datetime


DATA_FILE = os.path.join(os.path.dirname(__file__), "library.json")


# ── Classes ───────────────────────────────────────────────────
class Book:
    def __init__(self, title, author, genre, year, book_id=None):
        self.book_id   = book_id or self._generate_id()
        self.title     = title
        self.author    = author
        self.genre     = genre
        self.year      = year
        self.available = True
        self.issued_to = None
        self.issued_on = None

    def _generate_id(self):
        return f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def issue(self, member_name):
        if not self.available:
            return False, f"'{self.title}' is already issued to {self.issued_to}."
        self.available = False
        self.issued_to = member_name
        self.issued_on = datetime.now().strftime("%Y-%m-%d")
        return True, f"'{self.title}' issued to {member_name} on {self.issued_on}."

    def return_book(self):
        if self.available:
            return False, f"'{self.title}' is not currently issued."
        name = self.issued_to
        self.available = True
        self.issued_to = None
        self.issued_on = None
        return True, f"'{self.title}' returned by {name}. Thank you!"

    def to_dict(self):
        return {
            "book_id":   self.book_id,
            "title":     self.title,
            "author":    self.author,
            "genre":     self.genre,
            "year":      self.year,
            "available": self.available,
            "issued_to": self.issued_to,
            "issued_on": self.issued_on,
        }

    @classmethod
    def from_dict(cls, d):
        b = cls(d["title"], d["author"], d["genre"], d["year"], d["book_id"])
        b.available = d["available"]
        b.issued_to = d.get("issued_to")
        b.issued_on = d.get("issued_on")
        return b

    def __str__(self):
        status = "✅ Available" if self.available else f"📤 Issued → {self.issued_to}"
        return f"[{self.book_id}] {self.title} by {self.author} ({self.year}) | {self.genre} | {status}"


class Library:
    def __init__(self):
        self.books = {}    # book_id → Book

    def add_book(self, book):
        self.books[book.book_id] = book

    def remove_book(self, book_id):
        return self.books.pop(book_id, None)

    def find_by_id(self, book_id):
        return self.books.get(book_id.upper())

    def search(self, query, field="all"):
        q = query.lower()
        results = []
        for b in self.books.values():
            if field == "title"  and q in b.title.lower():  results.append(b)
            elif field == "author" and q in b.author.lower(): results.append(b)
            elif field == "genre"  and q in b.genre.lower():  results.append(b)
            elif field == "all" and (q in b.title.lower() or
                                     q in b.author.lower() or
                                     q in b.genre.lower()):
                results.append(b)
        return results

    def all_books(self, sort_by="title"):
        books = list(self.books.values())
        if sort_by == "title":  books.sort(key=lambda b: b.title.lower())
        elif sort_by == "author": books.sort(key=lambda b: b.author.lower())
        elif sort_by == "year":   books.sort(key=lambda b: b.year)
        return books

    def issued_books(self):
        return [b for b in self.books.values() if not b.available]

    # ── Persistence ───────────────────────────────────────────
    def save(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({bid: b.to_dict() for bid, b in self.books.items()}, f, indent=4)

    def load(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
                self.books = {bid: Book.from_dict(d) for bid, d in raw.items()}


# ── UI helpers ────────────────────────────────────────────────
def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║    📚  LIBRARY MANAGEMENT SYSTEM  📚   ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def show_menu(lib):
    total     = len(lib.books)
    available = sum(1 for b in lib.books.values() if b.available)
    issued    = total - available
    print(f"  ┌──────────────────────────────────────────┐")
    print(f"  │  📖 Total: {total:<5}  ✅ Available: {available:<5}  📤 Issued: {issued:<4}│")
    print(f"  ├──────────────────────────────────────────┤")
    print(f"  │   1  ➜  Add Book                         │")
    print(f"  │   2  ➜  View All Books                   │")
    print(f"  │   3  ➜  Search Books                     │")
    print(f"  │   4  ➜  Issue a Book                     │")
    print(f"  │   5  ➜  Return a Book                    │")
    print(f"  │   6  ➜  View Issued Books                │")
    print(f"  │   7  ➜  Delete a Book                    │")
    print(f"  │   8  ➜  Exit                             │")
    print(f"  └──────────────────────────────────────────┘")


def print_books(books, heading="Books"):
    if not books:
        print(f"\n  📭  No {heading.lower()} found.\n")
        return
    print(f"\n  ── {heading} ({len(books)}) ──────────────────────────")
    print(f"  {'#':<4} {'ID':<18} {'Title':<28} {'Author':<20} {'Year':<6} Status")
    print(f"  {'─'*4} {'─'*18} {'─'*28} {'─'*20} {'─'*6} {'─'*15}")
    for i, b in enumerate(books, 1):
        status = "✅" if b.available else f"📤 {b.issued_to[:10]}"
        title  = b.title[:26]  + ".." if len(b.title)  > 26 else b.title
        author = b.author[:18] + ".." if len(b.author) > 18 else b.author
        print(f"  {i:<4} {b.book_id:<18} {title:<28} {author:<20} {b.year:<6} {status}")
    print()


def add_book(lib):
    print("\n  ── Add New Book ──────────────────────────")
    title  = input("  📖  Title  : ").strip()
    author = input("  ✍️  Author : ").strip()
    genre  = input("  🏷️  Genre  : ").strip()
    while True:
        try:
            year = int(input("  📅  Year   : ").strip())
            break
        except ValueError:
            print("  ⚠️  Enter a valid year.")

    if not title or not author:
        print("  ⚠️  Title and Author are required.\n")
        return

    book = Book(title.title(), author.title(), genre.title(), year)
    lib.add_book(book)
    lib.save()
    print(f"\n  ✅  Book added!  ID: {book.book_id}")
    print(f"       '{book.title}' by {book.author}\n")


def search_books(lib):
    print("\n  ── Search ────────────────────────────────")
    print("  Search by: 1) All  2) Title  3) Author  4) Genre")
    field_map = {"1": "all", "2": "title", "3": "author", "4": "genre"}
    fc = input("  👉  Select (1-4): ").strip()
    field = field_map.get(fc, "all")
    query = input(f"  🔍  Enter {field} query: ").strip()
    results = lib.search(query, field)
    print_books(results, f"Results for '{query}'")


def issue_book(lib):
    print("\n  ── Issue Book ────────────────────────────")
    book_id = input("  🔢  Enter Book ID: ").strip()
    book = lib.find_by_id(book_id)
    if not book:
        print(f"  ❌  Book ID '{book_id}' not found.\n")
        return
    member = input("  👤  Member name  : ").strip().title()
    if not member:
        print("  ⚠️  Member name required.\n")
        return
    ok, msg = book.issue(member)
    print(f"\n  {'✅' if ok else '❌'}  {msg}\n")
    if ok:
        lib.save()


def return_book(lib):
    print("\n  ── Return Book ───────────────────────────")
    book_id = input("  🔢  Enter Book ID: ").strip()
    book = lib.find_by_id(book_id)
    if not book:
        print(f"  ❌  Book ID '{book_id}' not found.\n")
        return
    ok, msg = book.return_book()
    print(f"\n  {'✅' if ok else '❌'}  {msg}\n")
    if ok:
        lib.save()


def delete_book(lib):
    print("\n  ── Delete Book ───────────────────────────")
    book_id = input("  🔢  Enter Book ID to delete: ").strip()
    book = lib.find_by_id(book_id)
    if not book:
        print(f"  ❌  Book ID '{book_id}' not found.\n")
        return
    if not book.available:
        print(f"  ⚠️  Cannot delete — book is currently issued to {book.issued_to}.\n")
        return
    confirm = input(f"  ⚠️  Delete '{book.title}'? (yes/no): ").strip().lower()
    if confirm in ("yes", "y"):
        lib.remove_book(book.book_id)
        lib.save()
        print(f"  ✅  '{book.title}' deleted.\n")
    else:
        print("  ↩️  Cancelled.\n")


def main():
    show_banner()
    lib = Library()
    lib.load()
    print(f"  📂  {len(lib.books)} book(s) loaded from library.\n")

    while True:
        show_menu(lib)
        choice = input("\n  👉  Select (1-8): ").strip()

        if   choice == "1": add_book(lib)
        elif choice == "2":
            sort_by = input("\n  Sort by: 1) Title  2) Author  3) Year  [Enter=Title]: ").strip()
            sort_map = {"1": "title", "2": "author", "3": "year"}
            books = lib.all_books(sort_map.get(sort_by, "title"))
            print_books(books, "All Books")
        elif choice == "3": search_books(lib)
        elif choice == "4": issue_book(lib)
        elif choice == "5": return_book(lib)
        elif choice == "6":
            issued = lib.issued_books()
            print_books(issued, "Currently Issued Books")
        elif choice == "7": delete_book(lib)
        elif choice == "8":
            print(f"\n  ════════════════════════════════════════")
            print(f"  📚  Library saved. Goodbye! 👋\n")
            break
        else:
            print("\n  ⚠️  Invalid option! Select 1 to 8.\n")


if __name__ == "__main__":
    main()
