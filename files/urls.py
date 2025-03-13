from django.urls import path
from .views import (
    FolderContentsView, FolderCreateView, FileUploadView, FileDeleteView,
    FolderDeleteView, ImageUploadAPIview, ImageGetAPIview
)

urlpatterns = [
    path('<uuid:user_id>/folders/create/', FolderCreateView.as_view(), name="folder_create_root"),
    path('<uuid:user_id>/folders/<path:folder_path>/create/', FolderCreateView.as_view(), name="folder_create"),
    path("<uuid:user_id>/folders/delete/", FolderDeleteView.as_view(), name="folder_delete"),
    path("<uuid:user_id>/folders/<path:folder_path>/delete/", FolderDeleteView.as_view(), name="folder_delete"),
    path('<uuid:user_id>/folders/<path:folder_path>/upload/', ImageUploadAPIview.as_view(), name="image_upload"),
    path('<uuid:user_id>/folders/<path:folder_path>/<path:file>/', ImageGetAPIview.as_view(), name="image_retrieve"),
    path('<uuid:user_id>/<uuid:file_id>/delete/', FileDeleteView.as_view(), name='file_delete'),
    path('<uuid:user_id>/folders/', FolderContentsView.as_view(), name="folder_contents_root"),
    path('<uuid:user_id>/folders/<path:folder_path>/', FolderContentsView.as_view(), name="folder_contents"),
]
