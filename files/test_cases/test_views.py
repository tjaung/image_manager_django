from django.urls import reverse
from rest_framework import status
from .test_setup import TestSetup
from files.models import Folder  # ✅ Import Folder model
from rest_framework.authtoken.models import Token
from authentication.models import User
from rest_framework.test import APITestCase
import pdb

class TestFolderViews(APITestCase):

    def setUp(self):
        """✅ Set up test environment and inherit from TestSetup."""
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

        # Automatically authenticate all requests
        # self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.client.force_authenticate(user=self.user)

        # ✅ Assign `self.user` directly instead of `owner_id`
        self.root_folder = Folder.objects.create(
            name="Projects",
            owner_id=self.user,  # ✅ Ensure correct field name (`owner`, not `owner_id`)
        )

        self.folder_path = "Projects/Django"  # ✅ Example folder path inside "Projects"
        
        # ✅ Convert UUID to string before passing to `reverse()`
        self.create_folder_url = reverse(
            "folder_create",
            kwargs={"user_id": str(self.user.id), "folder_path": self.folder_path}  # ✅ Convert UUID to string
        )
        print(self.create_folder_url)



    def test_create_folder_successfully(self):
        """✅ Test if a logged-in user can create a folder inside a path."""
        folder_data = {"name": "Django"}

        res = self.client.post(self.create_folder_url, folder_data, format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("name", res.json())  # Ensure response includes folder name
        # pdb.set_trace()
        self.assertEqual(res.json()["name"], "Django")
        # pdb.set_trace()
        self.assertIn("path", res.json())  # ✅ Ensure response includes folder path
        # pdb.set_trace()
        self.assertEqual(res.json()["path"], "/Projects/Django")  # ✅ Check correct path
        # pdb.set_trace()

    def test_create_folder_without_name(self):
        """✅ Test that creating a folder without a name fails."""
        res = self.client.post(self.create_folder_url, {}, format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
