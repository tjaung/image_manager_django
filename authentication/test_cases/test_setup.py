from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class TestSetup(APITestCase):

    def setUp(self):
        # set up attributes for tests
        self.login_url = reverse("login")
        self.signup_url = reverse("signup")

        # data to send
        self.user_data = { 
            "username": "test", 
            "password": "Pass1234!", 
            "email": "test@mail.com" }
        self.login_data = {
            "username": "alreadyMadeUser",
            "password": "Pass1234!"
        }
        self.user = User.objects.create_user(
            username="alreadyMadeUser",
            email="test@gmail.com",
            password="Pass1234!"
        )

        # testing tokens
        self.token = Token.objects.create(user=self.user)
        self.test_token_url = reverse("test_token")  # Ensure this matches your urls.py

        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()