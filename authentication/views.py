from rest_framework.decorators import api_view;
from rest_framework.response import Response;

from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login(request):
    """
    Tries to log in a user and returns an authentication token if successful.
    
    Parameters:
        - username (str): username of the user
        - password (str): user's password

    Returns:
        - 200 OK: A JSON object containing the authentication token and user details.
        - 404 Not Found: If the user does not exist or the password is incorrect.
    """
    # try to find user
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    print(user.__str__)
    return Response({'token': token.key,
                    "user": serializer.data})

@api_view(['POST'])
def create_user(request):
    """
    Tries to create a new user with email, username, and a password
    given by the user. Returns a generated token and user details.

    Parameters:
        - email (str): email address of new user
        - username (str): username of new user
        - password (str): password of new user
    
    Returns:
        - 201 Created: A JSON object containing the authentication token and user details.
        - 400 Bad Request: If any required fields are missing or invalid.
    """

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # create user instance
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password']) # hash pwd
        user.save()
        # create token for user
        token = Token.objects.create(user=user)
        # return token in JSON so user can make api calls

        return Response({'token': token.key,
                        "user": serializer.data})
    
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    """
    Validates the authentication token.

    Headers:
        - Authorization: Token <your_auth_token>

    Returns:
        - 200 OK: Confirmation message that token is valid.
        - 403 Forbidden: If the token is invalid or not provided.
    """
    user = request.user

    return Response({
        "message": "Token is valid.",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "date_joined": user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
        }
    }, status=status.HTTP_200_OK)