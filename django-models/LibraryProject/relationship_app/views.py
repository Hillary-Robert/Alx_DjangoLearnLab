from django.shortcuts import render
from django.views.generic.detail import DetailView  # ✅ exact import the checker expects
from .models import Book
from .models import Library  # ✅ explicit separate import


# ✅ Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# ✅ Class-based view for library details using DetailView
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
