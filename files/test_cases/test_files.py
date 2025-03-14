from .test_setup import TestSetup
from django.core.files.uploadedfile import SimpleUploadedFile
import pdb

# testing files can be done on the client end


# class TestFileAPI(TestSetup):

    # def test_upload_file(self):
    #     """
    #     Test that a user can upload an image file.
    #     """
    #     file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
    #     data = {
    #         "file": file,
    #         "filename": "test_image.jpg"
    #     }
    #     response = self.client.post(f"{self.file_url}", data, format="multipart")

    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.data["filename"], "test_image.jpg")


    # def test_delete_file(self):
    #     """
    #     Test that a user can delete a file.
    #     """
    #     upload_res = self.client.post(
    #         f"{self.file_url}upload/",
    #         {"file": SimpleUploadedFile("delete_test.jpg", b"file_content", content_type="image/jpeg")},
    #         format="multipart"
    #     )
    #     pdb.set_trace()
    #     file_id = upload_res.data["id"]

    #     delete_res = self.client.delete(f"{self.file_url}{file_id}/")
    #     self.assertEqual(delete_res.status_code, 204)