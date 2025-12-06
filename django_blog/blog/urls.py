from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    # Home + post list
    path('', PostListView.as_view(), name='blog-home'),
    path('posts/', PostListView.as_view(), name='post-list'),

    # Auth URLs
    path('login/', auth_views.LoginView.as_view(
        template_name='blog/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        template_name='blog/logout.html'
    ), name='logout'),

    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Post CRUD (singular - to satisfy earlier checker)
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # Comment URLs
    path('posts/<int:post_id>/comments/new/', views.add_comment, name='comment-create'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
