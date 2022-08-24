"""
Serializers for task APIs
"""
from rest_framework import serializers

from core.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""

    class Meta:
        model = Task
        fields = [
            'id', 'track_id', 'order_major', 'order_minor',
            'task_name','ranges', 'learning_time', 'guideline'
        ]
        read_only_fields = ['id']


class TaskDetailSerializer(TaskSerializer):
    """Serializer for Task detail view."""

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['references']
