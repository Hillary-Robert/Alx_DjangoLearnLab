## 2. Retrieve
```python
from bookshelf.models import Book

# Retrieve the book instance with the title "1984"
book = Book.objects.get(title="1984")

print(book.id, book.title, book.author, book.publication_year)

# Expected output:
# 1 1984 George Orwell 1949
