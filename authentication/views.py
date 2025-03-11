from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from authentication.models import User  # ✅ Ensure using custom User model
from authentication.serializers import UserSerializer

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    """
    Login a user and return an authentication token.
    """
    user = get_object_or_404(User, username=request.data['username'])
    
    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)  # ✅ 401 instead of 404

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    """
    Create a new user and return an authentication token.
    """
    serializer = UserSerializer(data=request.data)
    
    if not serializer.is_valid():
        print("Serializer Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = serializer.save()
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    """
    Check if token authentication works.
    """
    user = request.user

    return Response({
        "message": "Token is valid.",
        "user": {
            "id": str(user.id),
            "username": user.username,
        }
    }, status=status.HTTP_200_OK)
