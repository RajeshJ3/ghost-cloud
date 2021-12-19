from django.db import models
import uuid

from django.contrib.auth.models import User
from datetime import datetime    

class FileType(models.Model):
    title = models.CharField(max_length=250)
    icon = models.CharField(max_length=32, default='file')

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

class Object(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='object_user')
    uuid = models.CharField(max_length=100, blank=True, null=True, unique=True)

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)

    belongs_to = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    OBJECT_TYPE_CHOICES = [
        ('DIR', 'Directory'),
        ('FILE', 'File'),
    ]
    object_type = models.CharField(max_length=32, choices=OBJECT_TYPE_CHOICES, default='FILE')

    # if 'object_type' is File
    file_type = models.ForeignKey('FileType', blank=True, null=True, on_delete=models.SET_NULL)
    size = models.IntegerField(blank=True, null=True)
    file = models.FileField(upload_to='objects/', blank=True, null=True)

    PRIVACY_STATUS_CHOICES = [
        ('PVT', 'Private'),
        ('PUB', 'Public'),
    ]
    privacy_status = models.CharField(max_length=32, choices=PRIVACY_STATUS_CHOICES, default='PVT')

    access_to = models.ManyToManyField(
        User,
        through='ObjectAccess',
        through_fields=('object', 'user'),
    )

    opened_on = models.DateTimeField(default=datetime.now, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            temp_uuid = uuid.uuid4()
            while Object.objects.filter(uuid=temp_uuid).count():
                temp_uuid = uuid.uuid4().hex
            self.uuid = temp_uuid

        super().save(*args, **kwargs)

class ObjectAccess(models.Model):
    object = models.ForeignKey('Object', on_delete=models.CASCADE, related_name='object_access_object')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='object_access_user')

    description = models.TextField(blank=True, null=True)

    RIGHTS_CHOICES = [
        ('VIEW', 'Viewer'),
        ('CMT', 'Commenter'),
        ('EDIT', 'Editor'),
    ]
    rights = models.CharField(max_length=32, choices=RIGHTS_CHOICES, default='VIEW')

    last_invited_on = models.DateTimeField(default=datetime.now, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.object)
