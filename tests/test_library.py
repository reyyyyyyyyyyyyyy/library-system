from datetime import date, timedelta

import pytest

from library import Library, LibraryError


@pytest.fixture
def lib():
    library = Library()
    library.add_book("978-0132350884", "Clean Code", "Robert Martin", copies=1)
    library.add_book("978-0201633610", "Design Patterns", "Gamma et al.", copies=2)
    library.register_member("M001", "Shreya")
    return library


# ---------- Books ----------
def test_add_book(lib):
    assert lib.books["978-0132350884"].title == "Clean Code"


def test_add_duplicate_book_raises_error(lib):
    with pytest.raises(LibraryError):
        lib.add_book("978-0132350884", "Clean Code", "Robert Martin")


def test_search_by_title_ignores_case(lib):
    results = lib.search_books("clean")
    assert [b.title for b in results] == ["Clean Code"]


def test_search_by_author(lib):
    assert len(lib.search_books("gamma")) == 1


# ---------- Members ----------
def test_register_duplicate_member_raises_error(lib):
    with pytest.raises(LibraryError):
        lib.register_member("M001", "Someone Else")


# ---------- Issue ----------
def test_issue_book_sets_due_date_14_days(lib):
    today = date(2026, 10, 1)
    loan = lib.issue_book("M001", "978-0132350884", today=today)
    assert loan.due_date == today + timedelta(days=14)
    assert lib.books["978-0132350884"].copies_available == 0


def test_issue_unavailable_book_rejected(lib):
    lib.register_member("M002", "Riya")
    lib.issue_book("M001", "978-0132350884")
    with pytest.raises(LibraryError):
        lib.issue_book("M002", "978-0132350884")


def test_issue_to_unknown_member_rejected(lib):
    with pytest.raises(LibraryError):
        lib.issue_book("M999", "978-0132350884")


def test_member_limit_of_3_books(lib):
    lib.add_book("111", "Book A", "X", copies=1)
    lib.add_book("222", "Book B", "Y", copies=1)
    lib.add_book("333", "Book C", "Z", copies=1)
    lib.issue_book("M001", "111")
    lib.issue_book("M001", "222")
    lib.issue_book("M001", "333")
    with pytest.raises(LibraryError):
        lib.issue_book("M001", "978-0201633610")


# ---------- Return and fine ----------
def test_return_on_time_no_fine(lib):
    issued = date(2026, 10, 1)
    lib.issue_book("M001", "978-0132350884", today=issued)
    fine = lib.return_book("M001", "978-0132350884", today=issued + timedelta(days=10))
    assert fine == 0
    assert lib.books["978-0132350884"].copies_available == 1


def test_return_late_charges_5_per_day(lib):
    issued = date(2026, 10, 1)
    lib.issue_book("M001", "978-0132350884", today=issued)
    fine = lib.return_book("M001", "978-0132350884", today=issued + timedelta(days=17))
    assert fine == 15  # 3 days late x Rs 5


def test_return_book_not_issued_rejected(lib):
    with pytest.raises(LibraryError):
        lib.return_book("M001", "978-0132350884")


def test_calculate_fine_never_negative():
    assert Library.calculate_fine(-4) == 0
