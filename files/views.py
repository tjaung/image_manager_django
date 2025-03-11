from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Folder, File, UploadImage
from .serializers import FolderSerializer, FileSerializer, UploadImageSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView



class FolderContentsView(ListAPIView):
    """
    List all folders and files inside a given path.
    """
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, user_id, folder_path=None):
        """
        Retrieve subfolders and files inside a specific folder.
        """
        print(f"Authenticated User: {request.user}")
        print(f"User ID from URL: {user_id}")
        print(f"Headers: {request.headers}")

        user = request.user  # Get authenticated user

        if folder_path:
            full_path = f"/{folder_path}"
            folder = get_object_or_404(Folder, owner_id=user, path=full_path)
        else:
            folder = None  # Root level

        subfolders = Folder.objects.filter(owner_id=user, parent_folder=folder)
        files = File.objects.filter(owner_id=user, folder=folder)

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

import os

class FolderCreateView(CreateAPIView):
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, user_id, folder_path=None, *args, **kwargs):
        user = request.user
        folder_name = request.data.get("name", None)

        if not folder_name:
            return Response({"error": "Folder name is required."}, status=status.HTTP_400_BAD_REQUEST)

        parent_folder = None  # Default: Root-level folder
        full_path = f"/{folder_name.strip('/')}"

        # ✅ Find the parent folder if this is a subfolder
        if folder_path:
            print("folder path: ", folder_path)
            parent_folder_path = f"/{folder_path.strip('/')}"  # Fix slashes
            print("parent folder: ", parent_folder_path)
            parent_folder = Folder.objects.filter(owner_id=user, path=parent_folder_path).first()

            if not parent_folder:
                return Response(
                    {"error": f"Parent folder '{folder_path}' does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            full_path = f"{parent_folder.path}/{folder_name.strip('/')}"
            print('parent folder: ', parent_folder)
        # else:
        #     full_path = f"/{folder_name.strip('/')}"

        # ✅ Create the new folder
        folder, created = Folder.objects.get_or_create(
            owner_id=user,
            name=folder_name.strip('/'),
            path=full_path,
            parent_folder=parent_folder
        )

        return Response(FolderSerializer(folder).data, status=status.HTTP_201_CREATED)


    
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

class ImageUploadAPIview(ListCreateAPIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileSerializer

    def post(self, request, user_id, folder_path=None):
        print("BEGIN POST")
        if "media" not in request.FILES:
            return Response({"error": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # make sure folder exists
        folder = None
        if folder_path:
            print("FOLDER PATH ", folder_path)
            full_path = f"/{folder_path.strip('/')}"
            folder = Folder.objects.filter(owner_id=user_id, path=full_path).first()
            print("Folder: ", folder)
            print(folder.id)
            if not folder:
                return Response(
                    {"error": f"Folder '{folder_path}' does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        # begin image upload
        print("BEGIN IMAGE UPLOAD")
        print(request.FILES.get("media"))
        imgData = analyzeFile(request.FILES.get("media"))
        print(imgData)
        serializer = FileSerializer(
            data = {
                "file": request.FILES.get("media"),
                "folder": folder.id,
                "path": full_path,
                "height": imgData["height"],
                "width": imgData["width"],
                "filesize": imgData['file_size'],
                "is_grayscale": imgData["is_grayscale"],
                "owner_id": user_id,
            },
            context={"request": request},
        )
        if serializer.is_valid():
            print("VALID SERIALIZER")
            serializer.save()
            return Response(
                {
                    "message": "Image uploaded successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    "message": serializer.errors,
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class ImageGetAPIview(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileSerializer

    def get(self, request, user_id, folder_path, file):
        print("request: ", request)
        print("user_id: ", user_id)
        print("folder path: ", folder_path)
        print("file: ", file)
        query = File.objects.filter(owner_id=user_id, path=f"/{folder_path}/{file}")
        serializer = FileSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from PIL import Image
def analyzeFile(file):
    if file == None:
        print("No file specified")

    image = Image.open(file)
    width, height = image.size
    is_grayscale = isGrayscale(image)
    file_size = file.size

    print(f"The image size is: {width}x{height} and file size is {file_size} bytes")
    print(f"The image is grayscale: {is_grayscale}")
    return {
        'width': width,
        'height': height,
        'file_size': file_size,
        'is_grayscale': is_grayscale
    }

def isGrayscale(img):
    img = img.convert("RGB")
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i,j))
            if r != g != b: 
                return False
    return True