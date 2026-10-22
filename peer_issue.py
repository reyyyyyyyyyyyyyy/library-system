ef iss(m, b):
    x = lib.books[b]
    if x.copies_available > 0:
        lib.loans.append([m, b, date.today()])
        x.copies_available = x.copies_available - 1
        print("done")