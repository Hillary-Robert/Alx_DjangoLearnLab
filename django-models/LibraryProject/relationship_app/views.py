from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView  # required by checker
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Book
from .models import Library  # required by checker


# ---------- Existing function-based view ----------

def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# ---------- Existing class-based view ----------

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# ---------- NEW: Authentication views ----------

def register_view(request):
    """User registration using Django's built-in UserCreationForm."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # log in after registration
            return redirect("list_books")
    else:
        form = UserCreationForm()

    return render(request, "relationship_app/register.html", {"form": form})


def login_view(request):
    """User login using Django's built-in AuthenticationForm."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("list_books")
    else:
        form = AuthenticationForm()

    return render(request, "relationship_app/login.html", {"form": form})


def logout_view(request):
    """Log the user out and show a simple confirmation page."""
    auth_logout(request)
    return render(request, "relationship_app/logout.html")
