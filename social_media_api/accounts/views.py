from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model


from .serializers import RegisterSerializer, UserProfileSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user)  # token already created in serializer
        return Response(
            {"token": token.key, "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == "GET":
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    serializer = UserProfileSerializer(
        request.user, data=request.data, partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        return Response({"error": "You cannot follow yourself."}, status=400)

    request.user.following.add(target_user)
    return Response({"message": f"You are now following {target_user.username}."}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        return Response({"error": "You cannot unfollow yourself."}, status=400)

    request.user.following.remove(target_user)
    return Response({"message": f"You unfollowed {target_user.username}."}, status=200)

