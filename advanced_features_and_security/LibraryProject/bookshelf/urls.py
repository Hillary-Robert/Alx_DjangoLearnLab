from django.urls import path
from . import views

app_name = "bookshelf"

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("books/new/", views.form_example, name="form_example"),
    path("books/create-demo/", views.book_create, name="book_create_demo"),
    path("books/<int:book_id>/edit-demo/", views.book_edit, name="book_edit_demo"),
    path("books/<int:book_id>/delete-demo/", views.book_delete, name="book_delete_demo"),
]
