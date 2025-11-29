from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer

    This serializer converts Book model instances to and from JSON.

    - It includes all fields of the Book model: id, title, publication_year, author.
    - It also contains custom validation to ensure that:
        * publication_year is not in the future.
    """

    class Meta:
        model = Book
        # "fields = '__all__'" includes every field from the Book model (id, title, publication_year, author)
        fields = "__all__"

    def validate_publication_year(self, value: int) -> int:
        """
        Field-level validation for publication_year.

        This method is automatically called when validating the publication_year field.

        Rules:
        - publication_year must not be greater than the current year.
        - If it is in the future, raise a ValidationError.
        """
        current_year = datetime.now().year

        if value > current_year:
            # DRF will transform this into a 400 Bad Request with error details in API responses.
            raise serializers.ValidationError(
                f"Publication year {value} cannot be in the future (current year is {current_year})."
            )

        # Always return the validated value
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer

    This serializer represents an Author along with all of their related Book objects.

    Relationship handling:
    - The Author model has a one-to-many relationship with Book via the 'author' ForeignKey.
    - In the Book model, we defined related_name='books', which lets us access all books for an author via:
        author.books.all()

    - Here, we define a 'books' field that uses the nested BookSerializer:
        books = BookSerializer(many=True, read_only=True)

      This means:
      * When we serialize an Author, we also include a list of their books.
      * Each book in that list is represented using BookSerializer.
      * 'many=True' indicates there can be multiple books for one author.
      * 'read_only=True' means we only use this field for output (GET),
        not for creating/updating books through AuthorSerializer.
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = [
            "id",
            "name",
            "books",  # nested list of books written by this author
        ]
