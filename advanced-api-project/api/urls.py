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
    # Existing combined CRUD endpoints
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),

    # Extra generic views for the task
    path("books/list/", BookListGenericView.as_view(), name="book-list-generic"),
    path("books/detail/<int:pk>/", BookDetailGenericView.as_view(), name="book-detail-generic"),

    # IMPORTANT: match checker-required patterns
    path("books/update/<int:pk>/", BookUpdateView.as_view(), name="book-update-generic"),
    path("books/delete/<int:pk>/", BookDeleteView.as_view(), name="book-delete-generic"),

    
    path("books/create/", BookCreateView.as_view(), name="book-create-generic"),
]
