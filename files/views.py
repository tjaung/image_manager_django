from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Folder, File
from .serializers import FolderSerializer, FileSerializer

class FolderContentsView(ListAPIView):
    """
    List all folders and files inside a given path.
    """
    permission_classes = [IsAuthenticated]

    def get_folder_contents(self, request, user_id, folder_path):
        """
        Retrieve subfolders and files inside a specific folder.
        """
        full_path = f"/{folder_path}"

        folder = get_object_or_404(Folder, owner_id=user_id, path=full_path)
        subfolders = Folder.objects.filter(owner_id=user_id, parent_folder=folder)
        files = File.objects.filter(owner_id=user_id, folder=folder)

        return Response({
            "folders": FolderSerializer(subfolders, many=True).data,
            "files": FileSerializer(files, many=True).data
        })

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Folder
from .serializers import FolderSerializer

class FolderCreateView(CreateAPIView):
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Validate the incoming data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        folder_path = self.kwargs.get('folder_path', '')

        parent_folder = None
        new_folder_name = None

        if folder_path:
            # If folder_path contains a slash, split it into parent and new folder name.
            if '/' in folder_path:
                parent_folder_path, new_folder_name = folder_path.rsplit('/', 1)
                # Look up the parent folder by its path.
                parent_folder = get_object_or_404(Folder, owner_id=user, path=f"/{parent_folder_path}")
            else:
                # If there's no slash, then there is no parent folder.
                new_folder_name = folder_path

        # Optionally, you could allow POST data to override the folder name.
        # For now we enforce the name from the URL:
        # Create the new folder by saving the serializer with additional fields.
        folder = serializer.save(owner_id=user, parent_folder=parent_folder, name=new_folder_name)

        # Construct the full path based on whether there's a parent folder.
        if parent_folder:
            folder.path = f"{parent_folder.path}/{new_folder_name}"
        else:
            folder.path = f"/{new_folder_name}"
        folder.save()

        # Re-serialize to include updated fields like the newly set path.
        response_serializer = self.get_serializer(folder)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

from rest_framework.parsers import MultiPartParser

class FileUploadView(CreateAPIView):
    """
    Upload a file inside a specific folder
    """
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]  # allows file uploads

    def upload_file(self, serializer):
        user = self.request.user
        folder_path = self.kwargs.get('folder_path', '')
        folder = None

        if folder_path:
            folder = get_object_or_404(Folder, owner_id=user, path=f"/{folder_path}")

        uploaded_file = serializer.save(owner_id=user, folder=folder)
        uploaded_file.path = f"{folder.path}/{uploaded_file.file.name}" if folder else f"/{uploaded_file.file.name}"
        uploaded_file.save()

from rest_framework.views import APIView
from rest_framework import status

class MoveRenameView(APIView):
    """
    Move or rename a file or folder
    """
    permission_classes = [IsAuthenticated]

    def refactor(self, request, user_id):
        """
        Move or rename a folder/file
        """
        item_type = request.data.get('type')  # "folder" or "file"
        old_path = request.data.get('old_path')
        new_path = request.data.get('new_path')

        if not old_path or not new_path:
            return Response({"error": "Both old_path and new_path are required"}, status=status.HTTP_400_BAD_REQUEST)

        if item_type == "folder":
            item = get_object_or_404(Folder, owner_id=user_id, path=old_path)
        elif item_type == "file":
            item = get_object_or_404(File, owner_id=user_id, path=old_path)
        else:
            return Response({"error": "Invalid type. Must be 'folder' or 'file'"}, status=status.HTTP_400_BAD_REQUEST)

        item.path = new_path
        item.name = new_path.split('/')[-1]  # Extract new folder/file name
        item.save()

        return Response({"message": f"{item_type} moved successfully", "new_path": item.path}, status=status.HTTP_200_OK)

class TrashView(APIView):
    """
    Soft-delete a file or folder (move to trash)
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        """
        Move file or folder to trash
        """
        item_type = request.data.get('type')  # "folder" or "file"
        path = request.data.get('path')

        if not path:
            return Response({"error": "Path is required"}, status=status.HTTP_400_BAD_REQUEST)

        if item_type == "folder":
            item = get_object_or_404(Folder, owner_id=user_id, path=path)
        elif item_type == "file":
            item = get_object_or_404(Image, owner_id=user_id, path=path)
        else:
            return Response({"error": "Invalid type. Must be 'folder' or 'file'"}, status=status.HTTP_400_BAD_REQUEST)

        item.path = f"/trash{item.path}"  # Move to trash
        item.save()

        return Response({"message": f"{item_type} moved to trash"}, status=status.HTTP_200_OK)


class RestoreView(APIView):
    """
    Restore a file or folder from trash
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """
        Restore an item from trash
        """
        item_type = request.data.get('type')
        path = request.data.get('path')

        if not path or not path.startswith("/trash"):
            return Response({"error": "Invalid trash path"}, status=status.HTTP_400_BAD_REQUEST)

        new_path = path.replace("/trash", "")

        if item_type == "folder":
            item = get_object_or_404(Folder, owner_id=user_id, path=path)
        elif item_type == "file":
            item = get_object_or_404(Image, owner_id=user_id, path=path)
        else:
            return Response({"error": "Invalid type. Must be 'folder' or 'file'"}, status=status.HTTP_400_BAD_REQUEST)

        item.path = new_path
        item.save()

        return Response({"message": f"{item_type} restored", "new_path": item.path}, status=status.HTTP_200_OK)
