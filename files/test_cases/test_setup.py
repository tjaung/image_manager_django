from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from authentication.models import User

class TestSetup(APITestCase):
    """
    Base test setup for authentication tests
    """

    def setUp(self):
        """
        Create a test user and generate a token
        """

        # Define API endpoint URLs
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")
        self.test_token_url = reverse("test_token")

        # Define test user data
        self.user_data = {
            "username": "testuser",
            "password": "Pass1234!"
        }

        # Create a test user in the database
        self.user = User.objects.create_user(
            username=self.user_data["username"],
            password=self.user_data["password"]
        )

        # Generate a token for the user
        self.token = Token.objects.create(user=self.user)

        # Store login credentials for reuse in tests
        self.login_data = {
            "username": self.user.username,
            "password": self.user_data["password"]
        }

        self.token = Token.objects.create(user=self.user)

        # Automatically authenticate all requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")


        return super().setUp()
    
    def tearDown(self):
        """Clean up after each test"""
        return super().tearDown()
