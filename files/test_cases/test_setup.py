from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from authentication.models import User

class TestSetup(APITestCase):
    def setUp(self):
        """
        Create a test user and authenticate them.
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!",
            # email="test@example.com"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.client.force_authenticate(user=self.user)
        self.folder_url = f"/api/{self.user.id}/folders/"
        self.file_url = f"/api/{self.user.id}/files/"

    def tearDown(self):
        """
        Clean up after tests.
        """
        return super().tearDown()
