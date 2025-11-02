## 4. Delete
\`\`\`python
from bookshelf.models import Book
b = Book.objects.get(title="Nineteen Eighty-Four")
b.delete()

# confirm deletion
print(Book.objects.all())  # Expected output: <QuerySet []>
\`\`\`
