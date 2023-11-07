from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User
from .models import Task
import json

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_files = ('username')

class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_important', 'date_completed', 'user', 'user_id']
        read_only_fields = ('date_completed', 'user',)  

# __DEVELOPMENT__
'''
class TaskDecoder(json.JSONDecoder):

    def decode(self, json_data):
        # Convert the JSON data to a dictionary
        data = json.JSONDecoder.decode(self, json_data)

        # Get the User object
        user = User.objects.get(id=data['user']['id'])

        # Create a Task object
        task = Task(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            is_important=data['is_important'],
            date_completed=data['date_completed'],
            user=user,
        )

        return task
        

class TaskDecoder(json.JSONDecoder):

    def __init__(self):
        super().__init__(object_hook=self._decode_object)

    def _decode_object(self, data):
        # if isinstance(data, list):
            print('llega acá es una lista')
            for task_data in data:
                return self._process_task(task_data)
                print('llega acá es una lista')
            #return [Task(**task_data) for task_data in data]
        #else:
        #    print('no es una lista')
        #    return self._process_task(data)

    def _process_task(self, task_data):
        print('llega a user')
        if 'user' in task_data:
            user_data = task_data.pop('user')
            # user = User(**user_data)
            user = User(
                id=user_data['id'],
                username=user_data['username'], 
                email=user_data['email']
                )
            task_data['user'] = user

        return Task(**task_data)
        


    # __DEVELOPMENT__
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     return Task.objects.create(
    #         title=validated_data['title'],
    #         description=validated_data['description'],
    #         is_important=validated_data['is_important'],
    #         user=user,
    #     )
'''