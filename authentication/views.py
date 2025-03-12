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
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    # Validate credentials...
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    res = Response({'token': token.key, "user": serializer.data}, status=status.HTTP_200_OK)
    refresh = RefreshToken.for_user(user)
    
    refresh_token = str(refresh)
    
    # Set the refresh token as an HTTP‑only cookie.
    res.set_cookie(
        key='access_token',
        value=token.key,  # your JWT refresh token
        httponly=True,
        secure=False,         # Set to True if using HTTPS in production
        samesite='Lax',       # or 'Strict'
        max_age=7 * 24 * 60 * 60  # Persist for one week (in seconds)
    )
    return res


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

@api_view(['POST'])
@csrf_exempt
def refresh_token(request):
    """
    Refresh the JWT access token using the refresh token from an HTTP‑only cookie.
    """
    print("Request cookies:", request.COOKIES)
    
    # Try to get the refresh token from cookies
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        print("No refresh token provided")
        return Response({'error': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)

    print("Refresh token from cookie:", refresh_token)
    
    serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
    try:
        serializer.is_valid(raise_exception=True)
    except TokenError as e:
        print("TokenError:", str(e))
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    print("Serializer validated data:", serializer.validated_data)
    
    new_access = serializer.validated_data.get('access')
    new_refresh = serializer.validated_data.get('refresh')  # May be None if ROTATE_REFRESH_TOKENS is False

    response = Response({'access': new_access}, status=status.HTTP_200_OK)

    # Set or re-set the refresh token cookie.
    # For development, set secure=False and add max_age.
    if new_refresh:
        response.set_cookie(
            key='refresh_token',
            value=new_refresh,
            httponly=True,
            secure=False,    # Change to True only in production (HTTPS)
            samesite='Lax',
            max_age=7 * 24 * 60 * 60  # 1 week
        )
    else:
        # Optionally, re-set the existing token with max_age even if it's not rotated.
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=False,    # Change to True in production
            samesite='Lax',
            max_age=7 * 24 * 60 * 60  # 1 week
        )
    return response
