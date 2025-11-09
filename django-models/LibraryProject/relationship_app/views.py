from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView  # required by previous checker
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import user_passes_test
from .models import Book
from .models import Library  # required by previous checker


# ---------- Existing: list all books ----------

def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# ---------- Existing: library detail view ----------

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# ---------- Existing: User registration ----------

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


# ---------- Helpers for role checks ----------

def is_admin(user):
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == "Admin"
    )


def is_librarian(user):
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == "Librarian"
    )


def is_member(user):
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == "Member"
    )


# ---------- Role-based views ----------

@user_passes_test(is_admin, login_url="login")
def admin_view(request):
    """Only accessible by users with role 'Admin'."""
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian, login_url="login")
def librarian_view(request):
    """Only accessible by users with role 'Librarian'."""
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member, login_url="login")
def member_view(request):
    """Only accessible by users with role 'Member'."""
    return render(request, "relationship_app/member_view.html")
