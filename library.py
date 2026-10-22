"""Library Management System - core logic (service layer)."""
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional

LOAN_DAYS = 14
MAX_BOOKS_PER_MEMBER = 3
FINE_PER_DAY = 10  # rupees


class LibraryError(Exception):
    """Raised when a library rule is broken."""


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    copies_total: int
    copies_available: int


@dataclass
class Member:
    member_id: str
    name: str


@dataclass
class Loan:
    member_id: str
    isbn: str
    issue_date: date
    due_date: date
    return_date: Optional[date] = None


class Library:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.loans = []

    # ---------- Books ----------
    def add_book(self, isbn, title, author, copies=1):
        if isbn in self.books:
            raise LibraryError(f"Book with ISBN {isbn} already exists")
        if copies < 1:
            raise LibraryError("Copies must be at least 1")
        self.books[isbn] = Book(isbn, title, author, copies, copies)
        return self.books[isbn]

    def search_books(self, query):
        q = query.lower()
        return [b for b in self.books.values()
                if q in b.title.lower() or q in b.author.lower() or q == b.isbn]

    # ---------- Members ----------
    def register_member(self, member_id, name):
        if member_id in self.members:
            raise LibraryError(f"Member {member_id} already exists")
        self.members[member_id] = Member(member_id, name)
        return self.members[member_id]

    def active_loans(self, member_id):
        return [l for l in self.loans
                if l.member_id == member_id and l.return_date is None]

    # ---------- Issue / Return ----------
    def issue_book(self, member_id, isbn, today=None):
        today = today or date.today()
        if member_id not in self.members:
            raise LibraryError("Member not found")
        book = self.books.get(isbn)
        if book is None:
            raise LibraryError("Book not found")
        if book.copies_available == 0:
            raise LibraryError("No copy available")
        if len(self.active_loans(member_id)) >= MAX_BOOKS_PER_MEMBER:
            raise LibraryError("Member already has 3 books")

        loan = Loan(member_id, isbn, today, today + timedelta(days=LOAN_DAYS))
        self.loans.append(loan)
        book.copies_available -= 1
        return loan

    def return_book(self, member_id, isbn, today=None):
        today = today or date.today()
        loan = next((l for l in self.active_loans(member_id) if l.isbn == isbn), None)
        if loan is None:
            raise LibraryError("No active loan found")
        loan.return_date = today
        self.books[isbn].copies_available += 1
        return self.calculate_fine((today - loan.due_date).days)

    @staticmethod
    def calculate_fine(days_late):
        return max(0, days_late) * FINE_PER_DAY
