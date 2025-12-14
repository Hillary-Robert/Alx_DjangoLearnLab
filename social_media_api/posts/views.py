from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # Search by title/content
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        """
        Optional: filter comments by post id using query param:
        /api/comments/?post=1
        """
        queryset = super().get_queryset()
        post_id = self.request.query_params.get("post")
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

    # Pagination (simple manual pagination using DRF paginator)
    from rest_framework.pagination import PageNumberPagination

    paginator = PageNumberPagination()
    paginator.page_size = 10
    page = paginator.paginate_queryset(posts, request)

    serializer = PostSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)

