## 2. Retrieve
\`\`\`python
from bookshelf.models import Book
books = Book.objects.all()
for book in books:
    print(book.id, book.title, book.author, book.publication_year)
# Expected output:
# 1 1984 George Orwell 1949
\`\`\`