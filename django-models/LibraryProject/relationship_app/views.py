from django.shortcuts import render
from django.views.generic import DetailView
# ✅ Import both models exactly as required
from .models import Book, Library



def list_books(request):
    
    books = Book.objects.all()

    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    # Explicit model import confirmed above
    model = Library
    
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
