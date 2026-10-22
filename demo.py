"""Small demo of the Library Management System (presentation layer)."""
from datetime import date, timedelta

from library import Library, LibraryError

lib = Library()
lib.add_book("978-0132350884", "Clean Code", "Robert Martin", copies=2)
lib.add_book("978-0201633610", "Design Patterns", "Gamma et al.")
lib.register_member("M001", "Shreya")

print("Search 'clean':")
for b in lib.search_books("clean"):
    print(f"  {b.title} by {b.author} - {b.copies_available} available")

issued = date(2026, 10, 1)
loan = lib.issue_book("M001", "978-0132350884", today=issued)
print(f"\nIssued 'Clean Code' to M001, due on {loan.due_date}")

fine = lib.return_book("M001", "978-0132350884", today=issued + timedelta(days=17))
print(f"Returned 3 days late. Fine: Rs {fine}")

try:
    lib.issue_book("M999", "978-0201633610")
except LibraryError as e:
    print(f"\nError: {e}")
