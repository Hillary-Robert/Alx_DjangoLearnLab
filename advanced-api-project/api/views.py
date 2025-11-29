from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListCreateAPIView):
    """
    BookListView

    This view provides:
    - GET /api/books/   -> list all books (with support for filtering, searching, ordering)
    - POST /api/books/  -> create a new book

    Filtering:
    - Uses DjangoFilterBackend to filter by:
        * title
        * publication_year
        * author (by author id)
        * author__name (by author name)

      Example:
        /api/books/?title=Things%20Fall%20Apart
        /api/books/?publication_year=1958
        /api/books/?author=1
        /api/books/?author__name=Chinua%20Achebe

    Searching:
    - Uses SearchFilter to perform partial text search on:
        * title
        * author__name

      Example:
        /api/books/?search=achebe
        /api/books/?search=things

    Ordering:
    - Uses OrderingFilter to order by:
        * title
        * publication_year
        * id

      Example:
        /api/books/?ordering=title
        /api/books/?ordering=-publication_year  (descending)
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Enable filtering, searching, and ordering for this view
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Fields for exact filtering (e.g. ?title=..., ?publication_year=...)
    filterset_fields = [
        "title",
        "publication_year",
        "author",        # filter by author id (e.g. ?author=1)
        "author__name",  # filter by author name (e.g. ?author__name=Chinua)
    ]

    # Fields to include in 'search='
    search_fields = [
        "title",
        "author__name",
    ]

    # Fields that can be used in 'ordering='
    ordering_fields = [
        "title",
        "publication_year",
        "id",
    ]

    # Default ordering if 'ordering=' is not specified
    ordering = ["title"]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    BookDetailView

    This view provides operations on a single book:
    - GET    /api/books/<id>/  -> retrieve a specific book
    - PUT    /api/books/<id>/  -> update all fields
    - PATCH  /api/books/<id>/  -> partially update
    - DELETE /api/books/<id>/  -> delete the book

    Note:
    - Filtering/searching/ordering are for list views, so they are
      not used here. This view only deals with a single book at a time.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
