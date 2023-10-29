from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'is_important']

    def create(self, validated_data):
        user = self.context['request'].user
        return Tarea.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            is_important=validated_data['is_important'],
            user=user,
        )