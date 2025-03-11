from django.urls import reverse
from rest_framework import status
from .test_setup import TestSetup
from files.models import Folder  # ✅ Import Folder model

class TestFolderViews(TestSetup):

    def setUp(self):
        """✅ Set up test environment and inherit from TestSetup."""
        super().setUp()  # ✅ Call parent setup first

        # ✅ Assign `self.user` directly instead of `owner_id`
        self.root_folder = Folder.objects.create(
            name="Projects",
            owner=self.user,  # ✅ Ensure correct field name (`owner`, not `owner_id`)
        )

        self.folder_path = "Projects/Django"  # ✅ Example folder path inside "Projects"
        
        # ✅ Convert UUID to string before passing to `reverse()`
        self.create_folder_url = reverse(
            "folder_create",
            kwargs={"user_id": str(self.user.id), "folder_path": self.folder_path}  # ✅ Convert UUID to string
        )


    def test_create_folder_successfully(self):
        """✅ Test if a logged-in user can create a folder inside a path."""
        folder_data = {"name": "Django"}

        response = self.client.post(self.create_folder_url, folder_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("name", response.json())  # ✅ Ensure response includes folder name
        self.assertEqual(response.json()["name"], "Django")
        self.assertIn("path", response.json())  # ✅ Ensure response includes folder path
        self.assertEqual(response.json()["path"], "/Projects/Django")  # ✅ Check correct path

    def test_create_folder_without_name(self):
        """✅ Test that creating a folder without a name fails."""
        response = self.client.post(self.create_folder_url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
