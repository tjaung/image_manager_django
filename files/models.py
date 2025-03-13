from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
from django.db import models

from authentication.models import User


class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner_id = models.ForeignKey(User, related_name="folders", on_delete=models.CASCADE)
    parent_folder = models.ForeignKey(
        'self', null=True, blank=True, related_name='subfolders', on_delete=models.CASCADE
    )
    path = models.CharField(max_length=1024, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Auto generate folder path.
        """
        if self.parent_folder:
            self.path = f"{self.parent_folder.path}/{self.name}"
        else:
            self.path = f"/{self.name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.path

    
class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner_id = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    folder = models.ForeignKey(
        Folder, null=True, blank=True, related_name='files', on_delete=models.CASCADE
    )
    file = models.FileField(upload_to='uploads/')
    path = models.CharField(max_length=1024)
    filename = models.CharField(max_length=1024, default='')
    width = models.IntegerField()
    height = models.IntegerField()
    filesize = models.IntegerField()
    is_grayscale = models.BooleanField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Auto generate file path.
        """
        if self.folder:
            self.path = f"{self.folder.path}/{self.file.name}"
        else:
            self.path = f"/{self.file.name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.path