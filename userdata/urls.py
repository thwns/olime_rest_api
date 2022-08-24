"""
URL mappings for the userdata app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from userdata import views


router = DefaultRouter()
router.register('userdatas', views.UserDataViewSet)

app_name = 'userdata'

urlpatterns = [
    path('', include(router.urls)),
]