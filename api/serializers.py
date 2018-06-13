'''
Serializers for all the things
'''
from rest_framework import serializers
from .models import (
    Process,
    ProcessDefinition,
    ProcessTask,
    RegisteredTask
)

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


class ProcessSerializer(serializers.ModelSerializer):
    """Simple serializer for professions"""
    class Meta:
        model = Process
        fields = '__all__'