from django.urls import reverse
from rest_framework import status
from .test_setup import TestSetup
from files.models import Folder  # ✅ Import Folder model
from rest_framework.authtoken.models import Token
from authentication.models import User
from rest_framework.test import APITestCase
import pdb

class TestFolderViews(TestSetup):

    def test_create_folder(self):
        """
        Test that a user can create a folder.
        """
        data = {"name": "New Folder"}
        response = self.client.post(f"{self.folder_url}", data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "New Folder")

    def test_list_folders(self):
        """
        Test that a user can retrieve the list of folders.
        """
        response = self.client.get(self.folder_url)
        pdb.set_trace()
        self.assertEqual(response.status_code, 200)

    def test_folder_detail_not_found(self):
        """
        Test that accessing a non-existent folder returns a 404.
        """
        response = self.client.get(f"{self.folder_url}/999")
        # pdb.set_trace()
        self.assertEqual(response.status_code, 404)

    def test_delete_folder(self):
        """
        Test deleting a folder.
        """
        create_res = self.client.post(f"{self.folder_url}", {"name": "DeleteMe"}, format="json")
        # pdb.set_trace()
        folder_id = create_res.data["id"]
        # pdb.set_trace()

        delete_res = self.client.delete(f"{self.folder_url}{folder_id}/")
        self.assertEqual(delete_res.status_code, 204)