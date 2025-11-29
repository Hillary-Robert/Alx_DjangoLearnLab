from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters_django  # required import for checks

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


# ----------------------------------------------------------------------
# Extra generic views for Task 1 (separate List, Detail, Create, Update, Delete)
# ----------------------------------------------------------------------

class BookListGenericView(generics.ListAPIView):
    """
    BookListGenericView

    Read-only list view for all books using DRF's generic ListAPIView.

    - URL: /api/books/list/
    - Method: GET

    Permissions:
    - Unauthenticated users: can read (list books).
    - Authenticated users: can also read.

    This view also supports filtering, searching, and ordering, similar
    to BookListView, but does not allow creating books.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "title",
        "publication_year",
        "author",
        "author__name",
    ]
    search_fields = [
        "title",
        "author__name",
    ]
    ordering_fields = [
        "title",
        "publication_year",
        "id",
    ]
    ordering = ["title"]


class BookDetailGenericView(generics.RetrieveAPIView):
    """
    BookDetailGenericView

    Read-only detail view for a single book using RetrieveAPIView.

    - URL: /api/books/<pk>/detail/
    - Method: GET

    Permissions:
    - Unauthenticated users: can read (retrieve).
    - Authenticated users: can also read.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    BookCreateView

    Create view for adding a new book using CreateAPIView.

    - URL: /api/books/create/
    - Method: POST

    Permissions:
    - Only authenticated users can create books.

    Validation:
    - Uses BookSerializer which enforces custom rules such as ensuring
      publication_year is not in the future.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Hook called when a new Book instance is being saved.

        Custom logic can be added here (such as attaching the current user).
        Currently, it simply saves the instance.
        """
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    BookUpdateView

    Update view for modifying an existing book using UpdateAPIView.

    - URL: /api/books/<pk>/update/
    - Methods: PUT, PATCH

    Permissions:
    - Only authenticated users can update books.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Hook called when updating an existing Book instance.

        Additional custom behavior can be added here if needed.
        """
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    BookDeleteView

    Delete view for removing a book using DestroyAPIView.

    - URL: /api/books/<pk>/delete/
    - Method: DELETE

    Permissions:
    - Only authenticated users can delete books.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
