"""
Serializers for profile APIs
"""
from rest_framework import serializers

from core.models import User_Data
from track.serializers import TrackSerializer


class UserDataSerializer(serializers.ModelSerializer):
    """Serializer for userdatas."""
    #track = TrackSerializer()

    class Meta:
        model = User_Data
        fields = [
            'id', 'track_id', 'action_date','order_major', 'order_minor',
            'is_done',
         ]
        read_only_fields = ['id']


class UserDataDetailSerializer(UserDataSerializer):
    """Serializer for UserData detail view."""

    class Meta(UserDataSerializer.Meta):
        fields = UserDataSerializer.Meta.fields + ['is_done']