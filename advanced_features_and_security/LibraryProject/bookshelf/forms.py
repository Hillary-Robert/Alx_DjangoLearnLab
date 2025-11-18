from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    Safe form for creating/editing books using Django's built-in validation.
    """

    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]


class BookSearchForm(forms.Form):
    """
    Search form with basic validation to safely handle user input.
    """
    query = forms.CharField(
        max_length=100,
        required=False,
        label="Search",
        help_text="Enter part of the book title to search.",
    )
