"""
URL mappings for the profile app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from profiles import views


router = DefaultRouter()
router.register('profiles', views.ProfileViewSet)

app_name = 'profiles'

urlpatterns = [
    path('', include(router.urls)),
]