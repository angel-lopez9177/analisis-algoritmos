from collections import Counter
def get_book_values(book_name):
    f = open(book_name)
    book_string = f.read()
    counting = Counter(book_string)
    values = list(counting.items())
    return values