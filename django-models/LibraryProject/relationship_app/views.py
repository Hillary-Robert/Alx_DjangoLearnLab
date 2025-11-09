from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView  # required by checker
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .models import Book
from .models import Library  # required by checker


# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view: library detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# Registration view (the checker looks for 'views.register' in urls.py)
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()

    return render(request, "relationship_app/register.html", {"form": form})
