from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    login_view,
    logout_view,
    register_view,
)

urlpatterns = [
    path('', list_books, name='home'),  # optional: homepage -> books
    path('books/', list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Auth URLs
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]

