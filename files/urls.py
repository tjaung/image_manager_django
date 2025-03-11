from django.urls import path
from .views import (
    FolderContentsView, FolderCreateView, FileUploadView, 
    MoveRenameView, TrashView, RestoreView
)

urlpatterns = [
    # List folder contents
    path('<int:user_id>/folders/<path:folder_path>/', FolderContentsView.as_view(), name="folder_contents"),
    # Create a folder
    path('<int:user_id>/folders/<path:folder_path>/create/', FolderCreateView.as_view(), name="folder_create"),
    # Upload a file
    path('<int:user_id>/files/<path:folder_path>/upload/', FileUploadView.as_view(), name="file_upload"),
    # Move/Rename files & folders
    path('<int:user_id>/move/', MoveRenameView.as_view(), name="move"),
    # Trash/Delete
    path('<int:user_id>/trash/', TrashView.as_view(), name="trash"),
    # Restore from Trash
    path('<int:user_id>/restore/', RestoreView.as_view(), name="restore"),
]
