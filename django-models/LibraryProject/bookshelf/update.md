## 3. Update
```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")   # or use get(id=1)
book.title = "Nineteen Eighty-Four"
book.save()

print(book.id, book.title, book.author, book.publication_year)

# Expected output:
# 1 Nineteen Eighty-Four George Orwell 1949
