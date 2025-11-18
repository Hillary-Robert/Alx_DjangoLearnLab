from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    ModelForm for creating/editing Book instances safely.
    """
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]


class BookSearchForm(forms.Form):
    """
    Search form with validation – used to safely handle user input
    in the book_list view.
    """
    query = forms.CharField(
        max_length=100,
        required=False,
        label="Search",
        help_text="Enter part of the book title to search.",
    )


class ExampleForm(forms.Form):
    """
    Example form used in form_example.html to demonstrate
    safe handling of user input and CSRF protection.
    """
    name = forms.CharField(max_length=100, required=True)
    message = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text="Optional message",
    )
