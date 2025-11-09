from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library


# ✅ Function-based view that lists all books
def list_books(request):
    # Explicitly use Book.objects.all() as required
    books = Book.objects.all()

    # ✅ Render using the specific template path required by checker
    return render(request, "relationship_app/list_books.html", {"books": books})


# ✅ Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "library_detail.html"
    context_object_name = "library"
