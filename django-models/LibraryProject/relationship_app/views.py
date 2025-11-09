from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView

from .models import Book, Library


# 1️⃣ Function-based view: list all books
def list_books(request):
    """
    Shows all books with their authors.
    Uses a template list_books.html if available.
    """
    books = Book.objects.select_related('author').all()

   

    return render(request, 'list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    """
    Shows details for one library and its books.
    URL will pass pk (id) of the library.
    """
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

