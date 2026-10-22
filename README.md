
def search_books(books, query):
    results = []
    for book in books:
        if query in book["title"]:
            results.append(book)
    return results