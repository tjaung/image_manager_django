from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Folder, File

class FolderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Folder
        fields = "__all__"

class FileSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = File
        fields = "__all__"
        