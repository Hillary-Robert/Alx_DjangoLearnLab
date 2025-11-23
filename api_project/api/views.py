from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly  # ✅ permissions

from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
   
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    Full CRUD API for Book model.

    Supports:
    - GET /books_all/          -> list
    - GET /books_all/{id}/     -> retrieve
    - POST /books_all/         -> create
    - PUT /books_all/{id}/     -> update
    - PATCH /books_all/{id}/   -> partial update
    - DELETE /books_all/{id}/  -> destroy
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
