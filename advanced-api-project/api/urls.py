from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookListGenericView,
    BookDetailGenericView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    # Existing combined CRUD endpoints (List + Create, Retrieve + Update + Delete)
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),

    # Separate generic views for Task 1
    path("books/list/", BookListGenericView.as_view(), name="book-list-generic"),
    path("books/<int:pk>/detail/", BookDetailGenericView.as_view(), name="book-detail-generic"),
    path("books/create/", BookCreateView.as_view(), name="book-create-generic"),
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update-generic"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete-generic"),
]
