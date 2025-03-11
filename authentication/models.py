from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """Custom manager for User model that supports username authentication"""

    def create_user(self, username, password=None):
        """Creates and returns a user with a username."""
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """Creates and returns a superuser."""
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model that replaces Django's default User model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True, default="default_user")
    password = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for Django Admin
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()  # ✅ Use updated `UserManager`

    USERNAME_FIELD = 'username'  # Users log in with username
    REQUIRED_FIELDS = []  # No additional required fields

    def __str__(self):
        return f"Username: {self.username}"
