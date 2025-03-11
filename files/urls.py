from django.urls import path
from .views import (
    FolderContentsView, FolderCreateView, FileUploadView, 
    MoveRenameView, TrashView, RestoreView, ImageUploadAPIview,
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
    # Upload Images
    path('<uuid:user_id>/folders/<path:folder_path>/upload/', ImageUploadAPIview.as_view(), name="image_upload"),
    path('<uuid:user_id>/folders/<path:folder_path>/<path:file>/', ImageGetAPIview.as_view(), name="image_retrieve"),
    # List folder contents (more general)
    path('<uuid:user_id>/folders/', FolderContentsView.as_view(), name="folder_contents_root"),
    path('<uuid:user_id>/folders/<path:folder_path>/', FolderContentsView.as_view(), name="folder_contents"),
    
    # Upload a file
    # path('<uuid:user_id>/folders/<path:folder_path>/upload/',debug_view),# ImageUploadAPIview.as_view(), name="file_upload"),
    # Move/Rename files & folders
    # path('<uuid:user_id>/move/', MoveRenameView.as_view(), name="move"),
    # Trash/Delete
    # path('<uuid:user_id>/trash/', TrashView.as_view(), name="trash"),
    # Restore from Trash
    # path('<uuid:user_id>/restore/', RestoreView.as_view(), name="restore"),
]
