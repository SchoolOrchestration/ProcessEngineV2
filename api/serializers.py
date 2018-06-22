'''
Serializers for all the things
'''
from rest_framework import serializers
from .models import (
    Process,
    ProcessDefinition,
    ProcessTask,
    RegisteredTask,
    Task,
    Result
)
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'
        exclude_fields = ('password',)


class RegisteredTaskSerializer(serializers.ModelSerializer):
    """Simple serializer for professions"""
    class Meta:
        model = RegisteredTask
        fields = '__all__'


class ProcessTaskSerializer(serializers.ModelSerializer):
    registered_task = RegisteredTaskSerializer(many=False, read_only=True)
    class Meta:
        model = ProcessTask
        fields = '__all__'
        # depth = 1

class ProcessDefinitionSerializer(serializers.ModelSerializer):
    """Simple serializer for professions"""
    tasks = ProcessTaskSerializer(source='processtask_set', read_only=True, many=True)
    class Meta:
        model = ProcessDefinition
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    result_set = ResultSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = '__all__'

class ProcessSerializer(serializers.ModelSerializer):
    """Simple serializer for professions"""
    task_set = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Process
        fields = '__all__'
        depth = 1