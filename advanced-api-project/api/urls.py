from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookListGenericView,
    BookDetailGenericView,
    BookCreateGenericView,
    BookUpdateGenericView,
    BookDeleteGenericView,
)

urlpatterns = [
    # Existing combined CRUD endpoints
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),

    # New separate generic views for Task 1
    path("books/list/", BookListGenericView.as_view(), name="book-list-generic"),
    path("books/<int:pk>/detail/", BookDetailGenericView.as_view(), name="book-detail-generic"),
    path("books/create/", BookCreateGenericView.as_view(), name="book-create-generic"),
    path("books/<int:pk>/update/", BookUpdateGenericView.as_view(), name="book-update-generic"),
    path("books/<int:pk>/delete/", BookDeleteGenericView.as_view(), name="book-delete-generic"),
]
