from relationship_app.models import Author, Book, Library, Librarian


# 1️⃣ Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        print(f"No author found with name '{author_name}'")
        return

    books = Book.objects.filter(author=author)
    print(f"Books by {author.name}:")
    for book in books:
        print(f"- {book.title}")


# 2️⃣ List all books in a specific library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")
        return

    print(f"Books in {library.name}:")
    for book in library.books.all():
        print(f"- {book.title} (Author: {book.author.name})")


# 3️⃣ Retrieve the librarian for a specific library (✅ uses Librarian.objects.get)
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")
        return

    try:
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for {library.name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"{library.name} has no librarian assigned")


if __name__ == "__main__":
    get_books_by_author("John Doe")
    get_books_in_library("Central Library")
    get_librarian_for_library("Central Library")
