# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.shortcuts import get_object_or_404
from .models import Folder, File
from authentication.models import User
from .serializers import FolderSerializer, FileSerializer
from rest_framework.decorators import action
from .utils import analyzeFile
from rest_framework.settings import api_settings

class FolderViewSet(viewsets.ViewSet):
    """
    A viewset that handles folder operations.
    
    Supported methods:
      - GET: List folder contents (folders and files) for a given path.
      - POST: Create a new folder.
      - PUT/PATCH: Move or rename a folder.
      - DELETE: Delete a folder.
    """
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = [IsAuthenticated]


    def list(self, request, user_id):
        """
        GET: List subfolders and files in the folder specified by the query parameter 'folder_path'.
        If no folder_path is provided, list items in the root.
        """
        # pull params
        user = request.user
        folder_path = request.query_params.get("folder_path", None)
        # dynamically grab folders depnding on if its the root level or a sub level
        if folder_path:
            full_path = f"/{folder_path}"
            folder = get_object_or_404(Folder, owner_id=user, path=full_path)
        else:
            folder = None  # root level

        # get all the folder contents and return them
        # Get all subfolders and files
        subfolders = Folder.objects.filter(owner_id=user, parent_folder=folder)
        files = File.objects.filter(owner_id=user, folder=folder)

        # ✅ Serialize objects before returning
        return Response({
            "folders": FolderSerializer(subfolders, many=True).data,
            "files": FileSerializer(files, many=True).data
        }, status=status.HTTP_200_OK)


    def create(self, request, user_id):
        """
        POST: Create a new folder.
        Optionally, you can pass a query parameter 'folder_path' to specify a parent folder.
        For example: POST /api/<user_id>/folders/?folder_path=docs/images
        """
        # pull params
        user = request.user
        folder_name = request.data.get("name")
        
        if not folder_name:
            return Response({"error": "Folder name is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve folder_path from query parameters
        folder_path = request.query_params.get("folder_path")
        parent_folder = None
        full_path = f"/{folder_name.strip('/')}"
        
        if folder_path:
            parent_folder_path = f"/{folder_path.strip('/')}"
            parent_folder = Folder.objects.filter(owner_id=user, path=parent_folder_path).first()
            if not parent_folder:
                return Response(
                    {"error": f"Parent folder '{folder_path}' does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            full_path = f"{parent_folder.path}/{folder_name.strip('/')}"

        # create folder
        folder, created = Folder.objects.get_or_create(
            owner_id=user,
            name=folder_name.strip('/'),
            path=full_path,
            parent_folder=parent_folder
        )

        return Response(FolderSerializer(folder).data, status=status.HTTP_201_CREATED)

    def update(self, request, user_id, pk=None):
        """
        PUT/PATCH: Move or rename a folder.
        Expects request data to include 'old_path' and 'new_path'.
        """
        user = request.user
        old_path = request.data.get('old_path')
        new_path = request.data.get('new_path')
        if not old_path or not new_path:
            return Response({"error": "Both old_path and new_path are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        folder = get_object_or_404(Folder, owner_id=user, path=old_path)
        folder.path = new_path
        folder.name = new_path.split('/')[-1]
        folder.save()
        return Response({"message": "Folder moved/renamed successfully", "new_path": folder.path}, status=status.HTTP_200_OK)

    def destroy(self, request, user_id, pk=None):
        user = request.user
        folder = get_object_or_404(Folder, owner_id=user, pk=pk)
        folder.delete()
        return Response({"message": "Folder deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

from rest_framework.parsers import MultiPartParser, FormParser

class FileViewSet(viewsets.ViewSet):
    """
    A viewset that handles file operations.
    
    Supported methods:
      - GET: Retrieve a file’s details.
      - POST: Upload a file.
      - PUT/PATCH: Move or rename a file.
      - DELETE: Delete a file.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, user_id):
        """
        GET: Retrieve a file by its path using query parameters.
        Expected query parameters:
        - user_id: Required, uuid
        - file_id: Required, uuid
        """

        file_id = request.query_params.get("file_id")
        user_id = request.query_params.get("user_id")

        if not file_id:
            return Response({"error": "file_name query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        file_instance = get_object_or_404(File, owner_id=user_id, id=file_id)
        serializer = FileSerializer(file_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, user_id, folder_path=None):
        """
        POST: Upload a file to the folder specified by `folder_path`.
        The folder path can be provided as a query parameter if not given in the URL.
        """
        user = get_object_or_404(User, id=user_id)
        # Get folder_path from query parameters
        folder_path = request.query_params.get("folder_path", folder_path)

        folder = None
        if folder_path:
            folder = get_object_or_404(Folder, owner_id=user, path=f"/{folder_path.strip('/')}")
        # pull image from request
        uploaded_file = request.FILES.get('file')
        filename = uploaded_file.name
        if not uploaded_file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Construct the file path: if a folder was found, use its path; otherwise, default to root which is none.
        file_path = f"{folder.path}/{filename}" if folder else f"/{filename}"
        imgData = analyzeFile(uploaded_file)

        # create serializer data for model
        serializer = FileSerializer(
            data={
                "file": uploaded_file,
                "folder": folder.id if folder else None,
                "path": file_path,  # Save the constructed file path
                "filename": filename,
                "height": imgData["height"],
                "width": imgData["width"],
                "filesize": imgData["file_size"],
                "is_grayscale": imgData["is_grayscale"],
                "owner_id": user_id,
            },
            context={"request": request},
        )
        # save
        if serializer.is_valid():
            file_obj = serializer.save(owner_id=user, folder=folder)
            file_obj.path = file_path  # Ensure the file path is set properly
            file_obj.save()
            return Response({"message": "File uploaded successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, user_id, pk=None):
        """
        PUT/PATCH: Move or rename a file.
        Expects request data to include 'old_path' and 'new_path'.
        """
        user = request.user
        old_path = request.data.get('old_path')
        new_path = request.data.get('new_path')
        if not old_path or not new_path:
            return Response({"error": "Both old_path and new_path are required."}, status=status.HTTP_400_BAD_REQUEST)
        file_obj = get_object_or_404(File, owner_id=user, path=old_path)
        file_obj.path = new_path
        file_obj.name = new_path.split('/')[-1]
        file_obj.save()
        return Response({"message": "File moved/renamed successfully", "new_path": file_obj.path}, status=status.HTTP_200_OK)

    def destroy(self, request, user_id, pk=None):
        """
        DELETE: Delete a file by its primary key.
        """
        file_obj = get_object_or_404(File, id=pk, owner_id=request.user.id)
        file_obj.delete()
        return Response({"message": "File deleted successfully."}, status=status.HTTP_204_NO_CONTENT)