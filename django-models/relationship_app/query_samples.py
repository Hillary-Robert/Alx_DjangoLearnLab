import os
import django

# Must use the internal Python package name with underscore
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def get_books_by_author(author_name):
    """Query all books by a specific author."""
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)


def get_books_in_library(library_name):
    """List all books in a library."""
    library = Library.objects.get(name=library_name)
    return library.books.all()


def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    library = Library.objects.get(name=library_name)
    return library.librarian


if __name__ == "__main__":
    print("Books by 'Author One':")
    for book in get_books_by_author("Author One"):
        print("-", book.title)

    print("\nBooks in 'Central Library':")
    for book in get_books_in_library("Central Library"):
        print("-", book.title)

    print("\nLibrarian for 'Central Library':")
    librarian = get_librarian_for_library("Central Library")
    print(librarian.name)
