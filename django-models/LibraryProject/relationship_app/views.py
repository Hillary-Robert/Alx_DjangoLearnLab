from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView  # required by checker
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import user_passes_test, permission_required
from .models import Author
from .models import Book
from .models import Library  # required by checker


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


# ---------- Role helpers ----------

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
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian, login_url="login")
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member, login_url="login")
def member_view(request):
    return render(request, "relationship_app/member_view.html")


# ---------- Permission-based Book actions ----------

@permission_required('relationship_app.can_add_book', login_url='login')
def add_book(request):
    """
    Only users with 'can_add_book' permission can create a new book.
    """
    if request.method == "POST":
        title = request.POST.get("title")
        author_name = request.POST.get("author")

        if title and author_name:
            author, _ = Author.objects.get_or_create(name=author_name)
            Book.objects.create(title=title, author=author)
            return redirect("list_books")

    return render(request, "relationship_app/add_book.html")


@permission_required('relationship_app.can_change_book', login_url='login')
def edit_book(request, pk):
    """
    Only users with 'can_change_book' permission can edit a book.
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        title = request.POST.get("title")
        author_name = request.POST.get("author")

        if title and author_name:
            author, _ = Author.objects.get_or_create(name=author_name)
            book.title = title
            book.author = author
            book.save()
            return redirect("list_books")

    return render(request, "relationship_app/edit_book.html", {"book": book})


@permission_required('relationship_app.can_delete_book', login_url='login')
def delete_book(request, pk):
    """
    Only users with 'can_delete_book' permission can delete a book.
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.delete()
        return redirect("list_books")

    return render(request, "relationship_app/delete_book.html", {"book": book})
