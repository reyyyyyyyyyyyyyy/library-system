def search_books(books, query):
    q = query.lower()
    return [book for book in books
            if q in book["title"].lower() or q in book["author"].lower()]

books = [
    {"title": "Clean Code", "author": "Robert Martin"},
    {"title": "Design Patterns", "author": "Gamma"},
]
print(search_books(books, "Clean"))
print(search_books(books, "clean"))
print(search_books(books, "martin"))