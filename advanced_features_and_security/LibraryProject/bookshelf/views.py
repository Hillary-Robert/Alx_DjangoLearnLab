from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book


@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    """
    Simple view that lists books.
    Only users with 'bookshelf.can_view' are allowed to access this.
    """
    books = Book.objects.all()
    titles = ", ".join(b.title for b in books)
    return HttpResponse(f"Books: {titles}")


@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    """
    Dummy create view for books.
    Only users with 'bookshelf.can_create' are allowed to access this.
    """
    return HttpResponse("Create Book – requires 'bookshelf.can_create' permission.")


@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, book_id):
    """
    Dummy edit view for a book.
    Only users with 'bookshelf.can_edit' are allowed to access this.
    """
    return HttpResponse(f"Edit Book {book_id} – requires 'bookshelf.can_edit' permission.")


@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, book_id):
    """
    Dummy delete view for a book.
    Only users with 'bookshelf.can_delete' are allowed to access this.
    """
    return HttpResponse(f"Delete Book {book_id} – requires 'bookshelf.can_delete' permission.")
