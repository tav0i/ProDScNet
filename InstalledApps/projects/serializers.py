from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']
        read_only_files = ('username')

class ProjectSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'technology', 'created_at', 'user', 'user_id')
        read_only_files = ('created_at', 'user')

