from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Folder, File

class FolderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Folder
        fields = "__all__"
        read_only_fields = ('path', 'owner_id',)

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"

    def create(self, validated_data):
        return File.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update instance with validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
