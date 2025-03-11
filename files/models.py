from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    """Custom User model that extends Django's AbstractUser"""
    
    groups = models.ManyToManyField(
        Group,
        related_name="files_users",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="files_user_permissions",
        blank=True
    )


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
    path = models.CharField(max_length=1024, unique=True)
    width = models.IntegerField()
    height = models.IntegerField()
    size = models.IntegerField()
    is_color = models.BooleanField()
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
