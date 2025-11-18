from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect

from .models import Book
from .forms import BookForm, BookSearchForm


@csrf_protect
@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    """
    Secure book list view.
    - Uses Django ORM (no raw SQL) to avoid SQL injection.
    - Uses a Django form to validate and clean search input.
    - Requires 'bookshelf.can_view' permission.
    """
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            # Safe filtering via ORM: protects against SQL injection
            books = books.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )

    context = {
        "books": books,
        "form": form,
    }
    return render(request, "bookshelf/book_list.html", context)


@csrf_protect
@permission_required("bookshelf.can_create", raise_exception=True)
def form_example(request):
    """
    Example create view for books.
    - Protected by CSRF.
    - Uses a ModelForm for validation and safe creation.
    - Requires 'bookshelf.can_create' permission.
    """
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            # Safe: uses Django ORM without raw SQL
            form.save()
            return redirect("bookshelf:book_list")
    else:
        form = BookForm()

    return render(request, "bookshelf/form_example.html", {"form": form})


@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    """
    Simple example endpoint to demonstrate 'can_create' permission check.
    """
    return HttpResponse("Create Book – requires 'bookshelf.can_create' permission.")


@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, book_id):
    """
    Example edit endpoint.
    In a real app, you would use a ModelForm and POST handling here.
    """
    # Just a simple placeholder using ORM safely:
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Edit Book {book.id} – requires 'bookshelf.can_edit' permission.")


@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, book_id):
    """
    Example delete endpoint.
    In a real app, you would typically only allow POST/DELETE for actual deletion.
    """
    # Just a simple placeholder using ORM safely:
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Delete Book {book.id} – requires 'bookshelf.can_delete' permission.")
