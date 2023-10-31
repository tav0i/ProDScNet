from rest_framework import serializers
from .models import Task, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nest the User serialization in Task

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_important', 'date_completed', 'user']
        read_only_files = ('date_completed',)

    # __DEVELOPMENT__
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     return Task.objects.create(
    #         title=validated_data['title'],
    #         description=validated_data['description'],
    #         is_important=validated_data['is_important'],
    #         user=user,
    #     )
