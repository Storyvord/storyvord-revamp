from rest_framework import serializers
from .models import File, Folder
from accounts.models import User
# import base64
# from django.core.files.base import ContentFile

# class Base64FileField(serializers.FileField):
#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:'):
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
#         return super().to_internal_value(data)


class FileSerializer(serializers.ModelSerializer):
    # file = Base64FileField(required=False, allow_null=True)
    allowed_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta:
        model = File
        fields = '__all__'

        
class FolderSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, required=False)
    class Meta:
        model = Folder 
        fields = ['id', 'description', 'icon', 'name', 'project', 'default', 'files']
        