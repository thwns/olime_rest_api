"""
Serializers for profile APIs
"""
from rest_framework import serializers

from core.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for profiles."""

    class Meta:
        model = Profile
        fields = ['id', 'nickname', 'role', 'image_url']
        read_only_fields = ['id']


class ProfileDetailSerializer(ProfileSerializer):
    """Serializer for Profile detail view."""

    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + ['subjects']
