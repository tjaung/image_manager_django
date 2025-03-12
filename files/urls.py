from django.urls import path
from .views import (
    FolderContentsView, FolderCreateView, FileUploadView, 
    MoveRenameView, FolderDeleteView, RestoreView, ImageUploadAPIview,
    ImageGetAPIview
)
from django.http import JsonResponse
def debug_view(request, *args, **kwargs):
    print(f"DEBUG: Incoming request -> {request.path}")
    return JsonResponse({"message": "This is a debug response!"})


urlpatterns = [
    # Create New folder
    path('<uuid:user_id>/folders/create/', FolderCreateView.as_view(), name="folder_create_root"),  # No parent folder
    path('<uuid:user_id>/folders/<path:folder_path>/create/', FolderCreateView.as_view(), name="folder_create"),
    path("<uuid:user_id>/folders/delete/", FolderDeleteView.as_view(), name="folder_delete"),
    path("<uuid:user_id>/folders/<path:folder_path>/delete/", FolderDeleteView.as_view(), name="folder_delete"),
    # Upload Images
    path('<uuid:user_id>/folders/<path:folder_path>/upload/', ImageUploadAPIview.as_view(), name="image_upload"),
    path('<uuid:user_id>/folders/<path:folder_path>/<path:file>/', ImageGetAPIview.as_view(), name="image_retrieve"),
    # List folder contents (more general)
    path('<uuid:user_id>/folders/', FolderContentsView.as_view(), name="folder_contents_root"),
    path('<uuid:user_id>/folders/<path:folder_path>/', FolderContentsView.as_view(), name="folder_contents"),
   
]