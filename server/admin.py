from django.contrib import admin
from authentication.models import User
from files.models import Folder, File

admin.site.register(User)
admin.site.register(Folder)
admin.site.register(File)
