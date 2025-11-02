
### CRUD_operations.md (combined)

cat > CRUD_operations.md <<'EOF'
# CRUD Operations for Book model

## 1. Create
\`\`\`python
from bookshelf.models import Book
b = Book(title="1984", author="George Orwell", publication_year=1949)
b.save()
print(b)  # Expected output: 1984
\`\`\`

## 2. Retrieve
\`\`\`python
from bookshelf.models import Book
books = Book.objects.all()
for book in books:
    print(book.id, book.title, book.author, book.publication_year)
# Expected output:
# 1 1984 George Orwell 1949
\`\`\`

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

## 4. Delete
\`\`\`python
from bookshelf.models import Book
b = Book.objects.get(title="Nineteen Eighty-Four")
b.delete()

# confirm deletion
print(Book.objects.all())  # Expected output: <QuerySet []>
\`\`\`
