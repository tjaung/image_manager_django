from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Folder, File, UploadImage

class FolderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Folder
        fields = "__all__"
        read_only_fields = ('path', 'owner_id',)

class FileSerializer(serializers.ModelSerializer):
    folder = serializers.StringRelatedField()
    
    class Meta(object):
        model = File
        fields = "__all__"
        
class UploadImageSerializer(serializers.ModelSerializer):
    folder = serializers.StringRelatedField()  # ✅ Show folder path instead of ID

    class Meta:
        model = UploadImage
        fields = ('id', 'image', 'uploaded_at', 'folder')