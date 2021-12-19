from rest_framework import serializers
from objects import models

class FileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileType
        fields = "__all__"

class ObjectSerializer(serializers.ModelSerializer):
    file_type = FileTypeSerializer()

    class Meta:
        model = models.Object
        fields = "__all__"

class ObjectAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ObjectAccess
        fields = "__all__"
