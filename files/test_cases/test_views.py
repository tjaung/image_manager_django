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
        # self.root_folder = Folder.objects.create(
        #     name="Projects",
        #     owner_id=self.user,  # ✅ Ensure correct field name (`owner`, not `owner_id`)
        # )

        self.folder_path = ""
        
        # ✅ Convert UUID to string before passing to `reverse()`
        # self.create_folder_url = reverse(
        #     "folder_create",
        #     kwargs={"user_id": str(self.user.id), "folder_path": self.folder_path}  # ✅ Convert UUID to string
        # )
        # print(self.create_folder_url)



    def test_create_folder_successfully(self):
        """✅ Test if a logged-in user can create a folder inside a path."""
        folder_data = {"name": "Django"}
        create_folder_url = reverse(
            "folder_create_root",
            kwargs={"user_id": str(self.user.id)}  # Convert UUID to string
        )
        # create root folder Django
        res = self.client.post(create_folder_url, folder_data, format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("name", res.json())  # Ensure response includes folder name
        self.assertEqual(res.json()["name"], "Django")
        self.assertIn("path", res.json())  # ✅ Ensure response includes folder path
        self.assertEqual(res.json()["path"], "/Django")  # Check correct path

        subfolder_name = "Django"
        subfolder_url = reverse(
            "folder_create", kwargs={"user_id": str(self.user.id), "folder_path": subfolder_name}
        )
        subfolder_data = {"name": "src"}  # Only "src", because "Django" is already in the URL
        
        res = self.client.post(subfolder_url, subfolder_data, format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("name", res.json())  # Ensure response includes folder name
        self.assertEqual(res.json()["name"], "src")
        self.assertIn("path", res.json())  # Ensure response includes folder path
        self.assertEqual(res.json()["path"], "/Django/src")  # check correct path

        # test the list of folders
        root_url = reverse(
            "folder_contents_root", kwargs={"user_id": str(self.user.id)}
        )
        res = self.client.get(root_url, format="json")
        # pdb.set_trace()
        self.assertIn("created_at", res.json()["folders"][0])
        self.assertEqual(res.json()["folders"][0]["name"], "Django")
        self.assertEqual(res.json()["folders"][0]["path"], "/Django")
        self.assertEqual(res.json()["folders"][0]["parent_folder"], None)
        

        # delete_url = reverse(
        #     "folder_delete", kwargs={"user_id": str(self.user.id), "folder_path": "Django"}
        # )
        # res = self.client.get(delete_url, format="json")
        # res = self.client.get(root_url, format="json")
        # pdb.set_trace()

    def test_create_folder_without_name(self):
        """Test that creating a folder without a name fails."""
        folder_data = {"name": ""}
        create_folder_url = reverse(
            "folder_create_root",
            kwargs={"user_id": str(self.user.id)}  # Convert UUID to string
        )
        # create root folder Django
        res = self.client.post(create_folder_url, folder_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
