## 3. Update
\`\`\`python
from bookshelf.models import Book
b = Book.objects.get(title="1984")   # or get(id=1)
b.title = "Nineteen Eighty-Four"
b.save()
print(b.id, b.title, b.author, b.publication_year)
# Expected output:
# 1 Nineteen Eighty-Four George Orwell 1949
\`\`\`