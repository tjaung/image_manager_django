# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FolderViewSet, FileViewSet

router = DefaultRouter()
# folder api routes
router.register(r'(?P<user_id>[0-9a-f-]+)/folders', FolderViewSet, basename='folder')
# ex: http://127.0.0.1:8000/api/93f1f27a-a81b-4a50-864c-66a95bec92cf/folders/create/

# file api routes
router.register(r'(?P<user_id>[0-9a-f-]+)/files', FileViewSet, basename='file')

urlpatterns = [
    path('', include(router.urls)),
]
