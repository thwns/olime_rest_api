"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from track import views


router = DefaultRouter()
router.register('tracks', views.TrackViewSet)
router.register('books', views.BookViewSet)
router.register('tasks', views.TaskViewSet)

app_name = 'track'

urlpatterns = [
    path('', include(router.urls)),
    path('track_all/', views.TrackAPIView.as_view()),
]
