"""
Views for the profile APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Profile
from profiles import serializers
# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    """View for manage profile APIs."""
    serializer_class = serializers.ProfileDetailSerializer
    queryset = Profile.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve profiles for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ProfileSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new profile."""
        serializer.save(user=self.request.user)