# Generated by Django 5.1.7 on 2025-03-13 17:00

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('path', models.CharField(max_length=1024, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folders', to=settings.AUTH_USER_MODEL)),
                ('parent_folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subfolders', to='files.folder')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='uploads/')),
                ('path', models.CharField(max_length=1024)),
                ('filename', models.CharField(default='', max_length=1024)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('filesize', models.IntegerField()),
                ('is_grayscale', models.BooleanField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL)),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='files.folder')),
            ],
        ),
    ]
