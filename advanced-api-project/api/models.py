from django.db import models


class Author(models.Model):
    """
    Author model

    This model represents a *single* author in the database.
    - name: The full name of the author.
    - Each Author can have many related Book objects (one-to-many relationship).
    """

    name = models.CharField(
        max_length=255,
        help_text="The full name of the author.",
    )

    def __str__(self) -> str:
        # Used in Django admin and shell to display a human-readable name
        return self.name


class Book(models.Model):
    """
    Book model

    This model represents a *single* book.
    Fields:
    - title: The title of the book.
    - publication_year: The year the book was published.
    - author: ForeignKey to Author, meaning:
        * One Author can be linked to MANY Book instances.
        * Each Book belongs to exactly one Author.
    """

    title = models.CharField(
        max_length=255,
        help_text="The title of the book.",
    )

    publication_year = models.IntegerField(
        help_text="The year the book was published (e.g. 2020).",
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",  # allows author.books to access all this author's books
        help_text="The author who wrote this book.",
    )

    def __str__(self) -> str:
        # Helpful for debugging and admin view
        return f"{self.title} ({self.publication_year})"
