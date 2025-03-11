from django.urls import path
from .views import (
    FolderContentsView, FolderCreateView, FileUploadView, 
    MoveRenameView, TrashView, RestoreView
)

urlpatterns = [
    # List folder contents
    path('<uuid:user_id>/folders/<path:folder_path>/create/', FolderCreateView.as_view(), name="folder_create"),
    # List folder contents (more general)
    path('<uuid:user_id>/folders/<path:folder_path>/', FolderContentsView.as_view(), name="folder_contents"),
    
    # Upload a file
    path('<uuid:user_id>/files/<path:folder_path>/upload/', FileUploadView.as_view(), name="file_upload"),
    # Move/Rename files & folders
    path('<uuid:user_id>/move/', MoveRenameView.as_view(), name="move"),
    # Trash/Delete
    path('<uuid:user_id>/trash/', TrashView.as_view(), name="trash"),
    # Restore from Trash
    path('<uuid:user_id>/restore/', RestoreView.as_view(), name="restore"),
]
